from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
)
from app.core.token_context import refreshed_tokens_ctx
from app.models.user import User

security = HTTPBearer()


def _load_user(db: Session, user_id: str | None) -> User:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def _issue_tokens_for_user(user: User, refresh_payload: dict) -> dict:
    access_expire_minutes = refresh_payload.get("access_expire_minutes")
    refresh_expire_minutes = refresh_payload.get("refresh_expire_minutes")

    access_token, access_token_expires_at = create_access_token(
        {"sub": str(user.id), "role": user.role},
        expire_minutes=access_expire_minutes,
    )
    refresh_token, refresh_token_expires_at = create_refresh_token(
        {
            "sub": str(user.id),
            "access_expire_minutes": access_expire_minutes,
            "refresh_expire_minutes": refresh_expire_minutes,
        },
        expire_minutes=refresh_expire_minutes,
    )

    return {
        "access_token": access_token,
        "access_token_expires_at": access_token_expires_at.isoformat(),
        "refresh_token": refresh_token,
        "refresh_token_expires_at": refresh_token_expires_at.isoformat(),
        "token_type": "bearer",
    }


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    x_refresh_token: str | None = Header(
        default=None,
        alias="X-Refresh-Token",
    ),
    db: Session = Depends(get_db),
) -> User:
    refreshed_tokens_ctx.set(None)
    access_token = credentials.credentials

    # 1) Try access token first
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        if payload.get("type") == "refresh":
            raise JWTError("Access token required")

        return _load_user(db, payload.get("sub"))
    except JWTError:
        pass

    # 2) Access invalid/expired → try refresh token
    if not x_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token. Refresh token required.",
        )

    try:
        refresh_payload = jwt.decode(
            x_refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        if refresh_payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user = _load_user(db, refresh_payload.get("sub"))
        tokens = _issue_tokens_for_user(user, refresh_payload)
        request.state.refreshed_tokens = tokens
        request.scope["refreshed_tokens"] = tokens
        refreshed_tokens_ctx.set(tokens)
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

import json

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.token_context import refreshed_tokens_ctx


class RefreshedTokenMiddleware(BaseHTTPMiddleware):
    """If auth refreshed tokens, attach them to the JSON response body + headers."""

    async def dispatch(self, request: Request, call_next):
        refreshed_tokens_ctx.set(None)
        response = await call_next(request)

        tokens = (
            request.scope.get("refreshed_tokens")
            or refreshed_tokens_ctx.get()
            or getattr(request.state, "refreshed_tokens", None)
        )
        if not tokens:
            return response

        response.headers["X-Access-Token"] = tokens["access_token"]
        response.headers["X-Access-Token-Expires-At"] = tokens[
            "access_token_expires_at"
        ]
        response.headers["X-Refresh-Token"] = tokens["refresh_token"]
        response.headers["X-Refresh-Token-Expires-At"] = tokens[
            "refresh_token_expires_at"
        ]
        response.headers["X-Token-Refreshed"] = "true"

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk if isinstance(chunk, bytes) else chunk.encode()

        try:
            data = json.loads(body.decode() or "null")
        except json.JSONDecodeError:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        if isinstance(data, dict):
            data.update(tokens)
            body = json.dumps(data).encode("utf-8")

        headers = {
            key: value
            for key, value in response.headers.items()
            if key.lower() != "content-length"
        }

        return Response(
            content=body,
            status_code=response.status_code,
            headers=headers,
            media_type="application/json",
        )

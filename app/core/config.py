# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT / Auth
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    FRONTEND_SUCCESS_URL: str
    FRONTEND_CANCEL_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"   # yeh line add ki hai


settings = Settings()
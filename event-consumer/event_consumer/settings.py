from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "SERVICE_NAME"
    service_password: str = "SERVICE_PASSWORD"
    secret_key: str = "SECRET_KEY"
    algorithm: str = "ALGORITHM"
    access_token_expire_minutes: int = "ACCESS_TOKEN_EXPIRE_MINUTES"

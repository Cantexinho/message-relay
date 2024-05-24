from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = (Field(..., env="SERVICE_NAME"),)
    service_password: str = Field(..., env="SERVICE_PASSWORD")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: str = Field(
        ..., env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

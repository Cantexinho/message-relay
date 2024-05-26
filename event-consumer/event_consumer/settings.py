from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str
    service_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class DatabaseSettings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_root_password: str
    mysql_database: str
    mysql_host: str
    mysql_port: int

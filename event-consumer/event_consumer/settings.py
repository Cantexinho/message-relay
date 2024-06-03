from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str
    service_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class DatabaseSettings(BaseSettings):
    # REVIEW COMMENT:
    # Nitpick, but IMO the naming is a bit redundant here.
    # Since it's a `DatabaseSettings` class, I think it makes it clear enough to remove the `mysql_` prefix from the attributes.
    mysql_user: str
    mysql_password: str
    mysql_root_password: str
    mysql_database: str
    mysql_host: str
    mysql_port: int

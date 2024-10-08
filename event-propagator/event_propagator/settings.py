from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str
    service_password: str
    scheduler_interval: str
    endpoint_to_post: str

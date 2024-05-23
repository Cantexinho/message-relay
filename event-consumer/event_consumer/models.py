from pydantic import BaseModel


class ServiceAuth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

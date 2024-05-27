"""
    Autherntication class used to authenticate api callers.
    Generates jwt token using oauth2
    and check if requests are made with this token.
    Authenticates to .env variables:
        - SERVICE_NAME = "service1"
        - SERVICE_PASSWORD = "service_password"

    -> get_current_user() - receives token and decodes it to check if
    username matches SERVICE_NAME = "service1".

    -> create_access_token() - creates token with provided
    algorythm and secret key.

    -> authenticate_user() - check if user credentials matches
        SERVICE_NAME = "service1"
        SERVICE_PASSWORD = "service_password"

    -> login_for_access_token() - function used to login user
    uses authenticate_user() to auth user and
    create_access_token() to create token to return.
"""

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from .schemas import ServiceAuth, Token
from .settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self):
        self.settings = Settings()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def get_current_user(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[self.settings.algorithm],
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        if username != self.settings.service_name:
            raise credentials_exception
        return username

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.settings.secret_key,
            algorithm=self.settings.algorithm,
        )
        return encoded_jwt

    def authenticate_user(self, username: str, password: str):
        if (
            username != self.settings.service_name
            or password != self.settings.service_password
        ):
            return False
        return ServiceAuth(username=username, password=password)

    async def login_for_access_token(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> Token:
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=int(self.settings.access_token_expire_minutes)
        )
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone
import os
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from .models import ServiceAuth, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(
        self,
        service_name: str,
        service_password: str,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
    ):
        self.service_name = service_name
        self.service_password = service_password
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        if username != os.environ.get("SERVICE_NAME"):
            raise credentials_exception
        return username

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def authenticate_user(self, username: str, password: str):
        if username != os.environ.get("SERVICE_NAME") or password != os.environ.get(
            "SERVICE_PASSWORD"
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
        access_token_expires = timedelta(minutes=int(self.access_token_expire_minutes))
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

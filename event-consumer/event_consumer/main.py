from fastapi import FastAPI, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from .models import ServiceAuth, Token
from .auth import AuthService

import os
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

origins = [
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


auth_service = AuthService(
    service_name=os.environ.get("SERVICE_NAME"),
    service_password=os.environ.get("SERVICE_PASSWORD"),
    secret_key=os.environ.get("SECRET_KEY"),
    algorithm=os.environ.get("ALGORITHM"),
    access_token_expire_minutes=os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
)


@app.get("/ready/")
async def ready_check():
    return Response(status_code=status.HTTP_200_OK, content="ok")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await auth_service.login_for_access_token(form_data)


@app.get("/events")
async def get_events(
    current_user: Annotated[ServiceAuth, Depends(auth_service.get_current_user)]
):
    return current_user

"""
    Main fastapi app.
    Uses cors to enable secure communication between
    the client-side web application and the server.

    Endpoints:

    -> GET /ready/ check to see if api is ready.

    -> GET /token/ returns token used for auth.
    Expects OAuth2PasswordRequestForm which requires:
        username: str
        password: str

    -> GET /events/ returns all events from events table.

    -> POST /events/ posts event to events table
    Expects EventCreate object:
        event_type: str
        event_payload: str
"""

from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ServiceAuth, Token, EventCreate
from .auth import AuthService

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from .database import DatabaseConnection

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

auth_service = AuthService()


@app.get("/ready/")
async def ready_check():
    return Response(status_code=status.HTTP_200_OK, content="ok")


@app.post("/token/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await auth_service.login_for_access_token(form_data)


@app.get("/events/")
async def get_events(
    current_user: Annotated[
        ServiceAuth, Depends(auth_service.get_current_user)
    ]
):
    db = DatabaseConnection()
    return db.get_all_events()


@app.post("/events/")
async def post_event(
    event_data: EventCreate,
    current_user: Annotated[
        ServiceAuth, Depends(auth_service.get_current_user)
    ],
):
    db = DatabaseConnection()
    try:
        db.post_event(event_data.event_type, event_data.event_payload)
        return {"status": "success"}
    except Exception as e:
        print(f"Error while processing event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

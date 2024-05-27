from pydantic import BaseModel, field_validator


class ServiceAuth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class EventCreate(BaseModel):
    event_type: str
    event_payload: str

    @field_validator("event_type")
    def validate_event_type(cls, value):
        if not isinstance(value, str):
            raise ValueError("Invalid event type")
        return value

    @field_validator("event_payload")
    def validate_event_payload(cls, value):
        if not isinstance(value, str):
            raise ValueError("Event payload must be a string")
        return value

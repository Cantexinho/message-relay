from pydantic import BaseModel, field_validator


class ServiceAuth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


"""
    Added validation to check if event type and payload are strings.
    From provided data it doesn`t seem logical for type and payload
    not to be strings so posting them should not be allowed.
"""


class EventCreate(BaseModel):
    event_type: str
    event_payload: str

    # REVIEW COMMENT:
    # These validators aren't necessary, since Pydantic performs this validation by default.
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

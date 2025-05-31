"""Module contains schemas for callback messages."""

from pydantic import BaseModel, Field

from typings.services import RequiredMessageContextDict


class CommandSchema[CodeType = str | None](BaseModel):
    """Command schema."""

    command_id: int
    text: str
    code: CodeType
    is_negative_feedback: bool


class MessageReferenceSchema(BaseModel):
    """Callback message schema with references on Storage."""

    text_filepath: str
    image_filepath: str | None
    required_data: RequiredMessageContextDict | None = Field(default=None)


class MessageSchema(BaseModel):
    """Callback message schema."""

    text: str
    image_url: str | None
    keyboard_buttons: list[CommandSchema] | None

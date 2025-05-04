"""Module contains schemas for callback messages."""

from pydantic import BaseModel


class MessageReferenceSchema(BaseModel):
    """Callback message schema with references on Storage."""

    text_filepath: str
    image_filepath: str | None


class MessageSchema(BaseModel):
    """Callback message schema."""

    text: str
    image_url: str | None

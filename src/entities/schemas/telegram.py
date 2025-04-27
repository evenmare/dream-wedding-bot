"""Module contains implementations of Telegram schemas."""

from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    """Telegram user schema."""

    id: int
    username: str

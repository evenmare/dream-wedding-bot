"""Module contains schemas for commands."""

from pydantic import BaseModel


class CommandSchema[CodeType = str | None](BaseModel):
    """Command schema."""

    command_id: int
    text: str
    code: CodeType
    is_negative_feedback: bool

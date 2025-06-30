"""Module contains schemas for notifications."""

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    """Notification schema."""

    notification_id: int
    code: str

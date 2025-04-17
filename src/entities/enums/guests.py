"""Module contains guest Enums."""

import enum


class GuestCategoryEnum(str, enum.Enum):
    """List of guest categories."""

    RELATIVE = "relative"
    FRIEND = "friend"
    WITNESS = "witness"


class GuestStatusEnum(str, enum.Enum):
    """List of guest stages."""

    INVITED = "invited"
    AWAITING_ANSWER = "awaiting_answer"
    DECLINED = "declined"
    CONFIRMED = "confirmed"

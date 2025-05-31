"""Module contatins entities Enums."""

from enum import Enum


class ContextEntityEnum(str, Enum):
    """Enum contains entities list."""

    GUEST = 'guests'
    GUEST_FORM = 'guests_forms'
    INVITATION_REQUEST = 'invitations_requests'

"""Module con"""

from typing import NamedTuple, Protocol, TYPE_CHECKING

from entities.schemas.forms import GuestFormSchema

if TYPE_CHECKING:
    from entities.schemas.forms import GuestFormSchema
    from entities.schemas.invitations import InvitationRequestSchema


class GuestInfoDataTuple(NamedTuple):
    """Guest info."""

    guest_form: 'GuestFormSchema'
    invitation_request: 'InvitationRequestSchema | None'


class HandleFormCallbackUseCaseProtocol(Protocol):
    """Protocol for form callbacks Use Cases."""

    should_delete_reply_keyboard: bool

    async def __call__(self, *, guest_form: 'GuestFormSchema', **__) -> GuestInfoDataTuple:
        ...

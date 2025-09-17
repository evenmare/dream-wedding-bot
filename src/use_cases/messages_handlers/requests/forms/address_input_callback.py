"""Module contains handler for INVITATION_ADDRESS_INPUT form stage."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.forms import GuestFormSchema
from entities.schemas.invitations import InvitationRequestSchema
from repositories.database.forms import GuestFormRepository
from repositories.database.invitations import InvitationRequestRepository
from services.get_address_by_location import GetAddressByLocationService
from typings.services import CoordinatesTuple
from typings.use_cases import GuestInfoDataTuple
from use_cases.messages_handlers.requests.forms.base import BaseHandleFormCallbackUseCase


class HandleAddressInputCallbackUseCase(BaseHandleFormCallbackUseCase):
    """Class contains INVITATION_ADDRESS_INPUT callback handler logic."""

    should_delete_reply_keyboard = True

    def __init__(
        self,
        guest_form_repository: GuestFormRepository,
        invitation_request_repository: InvitationRequestRepository,
        get_address_by_location_service: GetAddressByLocationService,
    ) -> None:
        """Class constructor.

        :param guest_form_repository: Guest form repository.
        :param invitation_reqest_repository: Invitation request repository.
        :param get_address_by_location_service: Get address by location service.
        """
        self.__guest_form_repository = guest_form_repository
        self.__invitation_request_repository = invitation_request_repository
        self.__get_address_by_location_service = get_address_by_location_service

    async def __call__(
        self,
        *,
        guest_form: GuestFormSchema,
        location: CoordinatesTuple | None,
        text: str | None,
    ) -> GuestInfoDataTuple:
        """Handle address input.

        :param guest_form: Guest form.
        :param location: Location.
        :return: Updated guest form.
        """
        if location:
            new_form_stage = GuestFormStageEnum.INVITATION_GEOTAG_VALIDATION
            address = await self.__get_address_by_location_service(coordinates=location)
        else:
            new_form_stage = GuestFormStageEnum.INVITATION_INFO_SPECIFICATION
            address = text

        guest_form.stage = new_form_stage
        await self.__guest_form_repository.partial_update(guest_form=guest_form)

        invitation_request = InvitationRequestSchema(guest_id=guest_form.guest_id, address=address)
        await self.__invitation_request_repository.partial_update(invitation_request=invitation_request)

        return GuestInfoDataTuple(
            guest_form=guest_form,
            invitation_request=invitation_request,
        )

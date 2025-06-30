"""Module contains message factory service implementation."""

from urllib.parse import urljoin

import jinja2

from configs.services import MessageFactoryServiceConfig
from entities.enums.entities import ContextEntityEnum
from entities.schemas.commands import CommandSchema
from entities.schemas.callbacks import MessageSchema
from entities.schemas.forms import GuestFormSchema
from entities.schemas.guests import GuestSchema
from entities.schemas.invitations import InvitationRequestSchema
from exceptions.services import RequiredContextWasNotProvidedException
from repositories.storages import StorageRepository
from typings.services import MessageFactoryDataTuple, RequiredMessageContextDict


class MessageFactoryService:
    """Message factory service."""

    def __init__(
        self,
        storage_repository: StorageRepository,
        config: MessageFactoryServiceConfig,
    ) -> None:
        """Class constructor.

        :param storage_config: Storage Config.
        :param storage_repository: Storage Repository.
        """
        self.__storage_repository = storage_repository
        self.config = config

    async def __call__(
        self,
        message_factory_data: MessageFactoryDataTuple[CommandSchema[str | None]],
        *,
        guest: GuestSchema | None = None,
        guest_form: GuestFormSchema | None = None,
        invitation_request: InvitationRequestSchema | None = None,
    ) -> MessageSchema:
        """Generate message from data.

        :param message_factory_data: Data for message factoring.
        :return: Message.
        """
        template_bytes = await self.__storage_repository.get_file(
            filename=message_factory_data.message_ref.text_filepath,
        )

        provided_context = {}
        if guest:
            provided_context[ContextEntityEnum.GUEST] = guest
        if guest_form:
            provided_context[ContextEntityEnum.GUEST_FORM] = guest_form
        if invitation_request:
            provided_context[ContextEntityEnum.INVITATION_REQUEST] = invitation_request

        message_text: str = self.__generate_text(
            template_bytes=template_bytes,
            required_context=message_factory_data.message_ref.required_data,
            provided_context=provided_context,
        )

        image_url = None
        if image_filepath := message_factory_data.message_ref.image_filepath:
            image_url = urljoin(self.config.BASE_FILES_URL, image_filepath)

        return MessageSchema(
            text=message_text,
            image_url=image_url,
            keyboard_buttons=message_factory_data.commands,
        )

    @staticmethod
    def __generate_text(
        template_bytes: bytes,
        *,
        required_context: RequiredMessageContextDict | None,
        provided_context: dict[ContextEntityEnum, GuestSchema | GuestFormSchema | InvitationRequestSchema],
    ) -> str:
        """Generate text from template and context.

        :param template_bytes: HTML template bytes.
        :param required_context: Required context for message generation.
        :param provided_context: Provided context for message generation.
        :return: Text for message.
        """
        environment = jinja2.Environment()
        template = environment.from_string(template_bytes.decode(encoding='utf-8'))

        template_context: dict[str, str | float] = {}

        if required_context:
            for entity_name, required_fields in required_context.items():
                try:
                    schema = provided_context[entity_name]
                except KeyError as exc:
                    if entity_name != ContextEntityEnum.INVITATION_REQUEST:
                        raise RequiredContextWasNotProvidedException from exc
                    schema = InvitationRequestSchema(guest_id=0)

                template_context.update(
                    {
                        f'{entity_name.value}__{field_name}': value
                        for field_name, value in schema.model_dump(include=set(required_fields)).items()
                    }
                )

        return template.render(template_context)

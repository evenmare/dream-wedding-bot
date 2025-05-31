"""Module contains service for update commands for gueest."""

from repositories.database.callbacks import CommandRepository


class UpdateAvailableCommandsService:
    """Service implements logic for update commands for guset."""

    def __init__(self, command_repository: CommandRepository):
        """Class constructor.

        :param command_repository: Repository for commands.
        """
        self.__command_repository = command_repository

    async def __call__(self, guests_ids: set[int]) -> None:
        """Synchronize guest's commands with public available commands list.

        :param guest: Guest schema.
        """
        public_commands_ids = {
            command.command_id async for command in self.__command_repository.filter_available()
        }

        guest_id_command_id_pairs: list[tuple[int, int]] = []
        for guest_id in guests_ids:
            guest_commands_ids = {
                command.command_id
                async for command in self.__command_repository.filter_available(guest_id=guest_id)
            }

            guest_id_command_id_pairs.extend(
                [(guest_id, command_id) for command_id in public_commands_ids - guest_commands_ids]
            )

        await self.__command_repository.make_available_for_guests(frozenset(guest_id_command_id_pairs))

"""Module contains base command implementation."""

import abc


class BaseCommand(abc.ABC):
    """Base command."""

    @property
    @abc.abstractmethod
    def command_name(self) -> str:
        """Command name."""
        raise NotImplementedError

"""Module contains Use Case's exceptions implementations."""

class NotAuthenticatedException(Exception):
    """User is not authenticated exception."""


class CommandNotFoundException(Exception):
    """Command not found exception."""

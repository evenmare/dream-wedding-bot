"""Module contains exceptions for services."""

class CallbackMessageNotFoundException(Exception):
    """Callback message not found exception."""


class RequiredContextWasNotProvidedException(Exception):
    """Required context was not provided."""

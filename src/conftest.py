import pytest  # noqa: F401


pytest_plugins = [
    'tests.fixtures.infrastractures',
    # init data
    'tests.fixtures.init_data.callback_messages',
    'tests.fixtures.init_data.guests',
    'tests.fixtures.init_data.forms',
    'tests.fixtures.init_data.invitations',
    'tests.fixtures.init_data.telegram',
]

"""Module implements logic for package applications run."""

import asyncio
import argparse

from dependency_injector.wiring import inject, Provide

from applications.bot.app import run_bot
from applications.commands import COMMANDS_MAPPING
from containers import Container
from infrastructures.databases import init_db
from repositories.storages import StorageRepository

# TODO: Refactoring
parser = argparse.ArgumentParser(prog='Dream Wedding Bot')
parser.set_defaults(name=None)

subparsers = parser.add_subparsers()

command_parser = subparsers.add_parser('run-command', help='Run selected command.')
command_parser.add_argument(
    '-n',
    '--name',
    type=str,
    help='Name of command.',
)


@inject
async def lifecycle(storage_repository: StorageRepository = Provide[Container.storage_repository]) -> None:
    """Runs an application."""
    # Lifespan
    await init_db()

    # Readiness
    await storage_repository.healthcheck()

    await run_bot()


@inject
async def run_command(command_name: str) -> None:
    """Runs a command."""
    # await init_db()
    await COMMANDS_MAPPING[command_name]()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    container = Container()
    container.wire(
        modules=[
            __name__,
        ],
        packages=[
            'applications',
            'services',
            'use_cases',
        ],
    )

    # TODO: refactoring
    coroutine = lifecycle()
    args = parser.parse_args()

    if command := COMMANDS_MAPPING.get(args.name):
        coroutine = command()()

    loop.run_until_complete(coroutine)

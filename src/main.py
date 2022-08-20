"""
Main module.
Configures logging and starts the bot.
"""

from logging import INFO, basicConfig

from bot.bot import run_bot
from db.client import initialize_database


def _main() -> None:
    _configure_logging()
    initialize_database()
    run_bot()


def _configure_logging() -> None:
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=INFO)


if __name__ == "__main__":
    _main()

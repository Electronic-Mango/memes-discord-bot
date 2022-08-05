"""
Module creating the bot, adding all required Cogs and running it.
"""

from os import getenv

from discord.ext.commands import Bot, when_mentioned_or
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")
COMMAND_PREFIX = getenv("COMMAND_PREFIX")


def run_bot() -> None:
    bot = Bot(command_prefix=when_mentioned_or(COMMAND_PREFIX))
    bot.run(DISCORD_BOT_TOKEN)

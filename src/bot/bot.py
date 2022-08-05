"""
Module creating the bot, adding all required Cogs and running it.
"""

from os import getenv

from discord.ext.commands import Bot, when_mentioned_or
from dotenv import load_dotenv

from bot.command.get import Get
from bot.event.on_command import OnCommand
from bot.event.on_connect import OnConnect
from bot.event.on_ready import OnReady

load_dotenv()
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")
COMMAND_PREFIX = getenv("COMMAND_PREFIX")


def run_bot() -> None:
    bot = Bot(command_prefix=when_mentioned_or(COMMAND_PREFIX))
    bot.add_cog(OnConnect(bot))
    bot.add_cog(OnReady(bot))
    bot.add_cog(OnCommand())
    bot.add_cog(Get())
    bot.run(DISCORD_BOT_TOKEN)

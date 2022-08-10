"""
Module creating the bot, adding all required Cogs and running it.
"""

from discord.ext.commands import Bot, when_mentioned_or

from bot.command.get import Get
from bot.command.pasta import Pasta
from bot.event.on_command import OnCommand
from bot.event.on_connect import OnConnect
from bot.event.on_ready import OnReady
from settings import BOT_COMMAND_PREFIX, BOT_TOKEN


def run_bot() -> None:
    bot = Bot(command_prefix=when_mentioned_or(BOT_COMMAND_PREFIX))
    bot.add_cog(OnConnect(bot))
    bot.add_cog(OnReady(bot))
    bot.add_cog(OnCommand())
    bot.add_cog(Get())
    bot.add_cog(Pasta())
    bot.run(BOT_TOKEN)

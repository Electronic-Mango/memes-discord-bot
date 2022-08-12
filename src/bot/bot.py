"""
Module creating the bot, adding all required Cogs and running it.
"""

from discord.ext.commands import Bot, when_mentioned_or

from bot.command.media import Media
from bot.command.text import Text
from bot.event.on_command import OnCommand
from bot.event.on_connect import OnConnect
from bot.event.on_ready import OnReady
from settings import BOT_COMMAND_PREFIX, BOT_TOKEN


def run_bot() -> None:
    """Create, configure and run the bot"""
    bot = Bot(command_prefix=when_mentioned_or(BOT_COMMAND_PREFIX))
    bot.add_cog(OnConnect(bot))
    bot.add_cog(OnReady(bot))
    bot.add_cog(OnCommand())
    bot.add_cog(Media())
    bot.add_cog(Text())
    bot.run(BOT_TOKEN)

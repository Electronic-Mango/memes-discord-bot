"""
Module creating the bot, adding all required Cogs and running it.
"""

from disnake.ext.commands import InteractionBot

from bot.command.help import HelpCog
from bot.command.media import MediaCog
from bot.command.text import TextCog
from bot.event.on_application_command import OnApplicationCommand
from bot.event.on_connect import OnConnect
from bot.event.on_ready import OnReady
from settings import BOT_TOKEN


def run_bot() -> None:
    """Create, configure and run the bot"""
    bot = InteractionBot()
    bot.add_cog(media_cog := MediaCog(bot))
    bot.add_cog(TextCog())
    bot.add_cog(HelpCog())
    bot.add_cog(OnApplicationCommand())
    bot.add_cog(OnConnect(bot))
    bot.add_cog(OnReady(bot, media_cog))
    bot.run(BOT_TOKEN)

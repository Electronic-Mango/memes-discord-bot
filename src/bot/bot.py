"""
Module creating the bot, adding all required Cogs and running it.
"""

from disnake.ext.commands import Bot

from bot.command.media import MediaCog
from bot.command.text import TextCog
from bot.event.on_application_command import OnApplicationCommand
from bot.event.on_connect import OnConnect
from bot.event.on_ready import OnReady
from settings import BOT_TOKEN


# TODO Perhaps a custom "help" command would be in order?
# Default one wasn't very useful, since it didn't cover slash commands.
def run_bot() -> None:
    """Create, configure and run the bot"""
    bot = Bot()
    bot.add_cog(MediaCog())
    bot.add_cog(OnConnect(bot))
    bot.add_cog(OnReady(bot))
    bot.add_cog(OnApplicationCommand())
    bot.add_cog(TextCog())
    bot.run(BOT_TOKEN)

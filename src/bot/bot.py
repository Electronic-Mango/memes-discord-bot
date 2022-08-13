"""
Module creating the bot, adding all required Cogs and running it.
"""

from discord.ext.commands import Bot

from bot.command.media import media_command_group
from bot.command.text import text_command_group
from bot.event.on_connect import OnConnect
from bot.event.on_ready import OnReady
from settings import BOT_TOKEN


# TODO Perhaps a custom "help" command would be in order?
# Default one wasn't very useful, since it didn't cover slash commands.
def run_bot() -> None:
    """Create, configure and run the bot"""
    bot = Bot(help_command=None)
    bot.add_cog(OnConnect(bot))
    bot.add_cog(OnReady(bot))
    bot.add_application_command(media_command_group)
    bot.add_application_command(text_command_group)
    bot.run(BOT_TOKEN)

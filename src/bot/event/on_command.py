"""
Event Cog logging all command calls.
"""

from logging import getLogger

from discord.ext.commands import Cog, Context


class OnCommand(Cog):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @Cog.listener()
    async def on_command(self, context: Context) -> None:
        server = context.guild.name if context.guild else context.guild
        channel = context.channel
        user = context.author
        command = context.command
        self._logger.info(f"[{server}] [{channel}] [{user}] [{command}]")

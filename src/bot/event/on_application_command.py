"""
Event Cog logging information about called command.
"""

from logging import getLogger

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog


class OnApplicationCommand(Cog):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @Cog.listener()
    async def on_application_command(self, context: ApplicationCommandInteraction) -> None:
        server = context.guild.name if context.guild else None
        channel = context.channel
        user = context.author
        command = context.application_command.qualified_name
        self._logger.info(f"[{server}] [{channel}] [{user}] [{command}]")

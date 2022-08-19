"""
Event Cog logging information about called command.
"""

from logging import getLogger

from disnake import CommandInteraction
from disnake.ext.commands import Cog


class OnApplicationCommand(Cog):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @Cog.listener()
    async def on_application_command(self, interaction: CommandInteraction) -> None:
        source = f"[{interaction.guild}] [{interaction.channel}]" if interaction.guild else "[DM]"
        user = interaction.author
        command = interaction.application_command.qualified_name
        self._logger.info(f"{source} [{user}] [{command}]")

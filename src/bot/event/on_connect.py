"""
Event Cog logging information about connection establishment.
"""

from logging import getLogger

from disnake import Client
from disnake.ext.commands import Cog


class OnConnect(Cog):
    def __init__(self, bot: Client) -> None:
        self._bot = bot
        self._logger = getLogger(__name__)

    @Cog.listener()
    async def on_connect(self) -> None:
        self._logger.info(f"[{self._bot.user}] connected")

"""
Command Cog sending back a random meme.
"""

from aiohttp import ClientSession
from io import BytesIO

from discord import File
from discord.ext.commands import Cog, Context, command

from image_getter import get_random_image_url


class Get(Cog, name="Get a random meme"):
    @command(name="get")
    async def get(self, context: Context) -> None:
        """Get a random meme"""
        meme_url = get_random_image_url()
        image_bytes = await self._load_image(meme_url)
        await context.send(file=File(image_bytes, meme_url))
    

    async def _load_image(self, url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())

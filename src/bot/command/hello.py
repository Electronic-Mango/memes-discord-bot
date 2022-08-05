"""
Command Cog sending a "Hello!" back to the user.
Used for development purposes.
"""

from discord.ext.commands import Cog, Context, command


class Hello(Cog, name="Say hello to the bot"):
    @command(name="hello")
    async def hello(self, context: Context) -> None:
        """Say hello to the bot"""
        await context.reply("Hello!")

import discord
from discord.ext import commands
from main import GeminiBot


class Events(commands.Cog):
    def __init__(self, bot: GeminiBot):
        self.bot = bot

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        """
        Sends a message when the bot joins a guild.
        """
        if self.bot.log_channel:
            await self.bot.log_channel.send(
                f"Joined {guild.name} (ID: {guild.id}) with {guild.member_count} members. Current guild count: {len(self.bot.guilds)}"
            )
    
    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: discord.Guild):
        """
        Sends a message when the bot leaves a guild.
        """
        if self.bot.log_channel:
            await self.bot.log_channel.send(
                f"Left {guild.name} (ID: {guild.id}) with {guild.member_count} members. Current guild count: {len(self.bot.guilds)}"
            )


async def setup(bot: GeminiBot):
    await bot.add_cog(Events(bot))

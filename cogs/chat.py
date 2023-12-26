import discord
from discord.ext import commands
from main import GeminiBot
from helpers.session import Session

class Chat(commands.Cog):
    def __init__(self, bot: GeminiBot):
        self.bot = bot
        self.sessions = {}
        self.messages = []

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        """
        Checks whether the message starts with the bot's mention, if the author is blacklisted, or if the author is a bot.
        """
        if message.author.id in self.bot.config.get("blacklist") or message.author.bot:
            return
        
        if not message.content.startswith(self.bot.user.mention) and (message.reference is None or message.reference.message_id not in self.messages):
            return
        
        if message.channel.type == discord.ChannelType.private:
            return await message.channel.send("Please use me in a server, not in DMs.")
        
        if message.author.id in self.sessions:
            session = self.sessions[message.author.id]
        else :
            session = Session(self.bot, author=message.author, channel=message.channel, guild=message.guild)
            self.sessions[message.author.id] = session
            await session.initialize()

        async with message.channel.typing():
            response = await session.send(message.content, message.attachments)

        message = await message.reply(response)

        self.messages.append(message.id)

    @commands.command()
    async def reset(self, ctx: commands.Context):
        """
        Resets the session.
        """
        if ctx.author.id in self.sessions:
            del self.sessions[ctx.author.id]
        await ctx.send("Reset your session.")

    @commands.command()
    async def delete_last(self, ctx: commands.Context, amount: int = 1):
        """
        Deletes the last message sent by the bot.
        """
        session: Session = self.sessions.get(ctx.author.id, None)
        if session is None:
            await ctx.send("You have no active session.")
            return
        
        if amount > len(session.history):
            await ctx.send("You cannot delete more messages than you have sent.")
            return
        
        for _ in range(amount):
            message_id = session.history.pop()
            try:
                message = await ctx.channel.fetch_message(message_id)
            except discord.NotFound:
                await message.reply("Message not found, either it was deleted, or not in this channel.")
                return
            await message.delete()

        await ctx.send(f"Deleted {amount} messages.")

    @commands.is_owner()
    @commands.command()
    async def history(self, ctx: commands.Context, user: discord.User = None):
        """
        Shows the history of the current session.
        """
        if user is None:
            user = ctx.author

        session: Session = self.sessions.get(user.id, None)
        if session is None:
            await ctx.send("You have no active session.")
            return

        resp = f"History of **{user.name}**:\n\n"

        for message in session.history:
            resp += f"**{message['role']}**: {message['parts'][0]['text']}\n"

        await ctx.send(resp)

        
async def setup(bot: GeminiBot):
    await bot.add_cog(Chat(bot))

        

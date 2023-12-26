import discord
from discord.ext import commands
from discord.ui import View, Button
from main import GeminiBot
from helpers.session import Session

class Chat(commands.Cog):
    def __init__(self, bot: GeminiBot):
        self.bot = bot
   
    @commands.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title="Gemini Bot")
        embed.description = f"Hi, I'm {self.bot.user.name}! I'm a chatbot that uses the state-of-the-art Google Gemini AI to chat with you. I'm still in development, so please be patient with me. If you have any questions, please contact my owner, {self.bot.config.get('owner', 'unknown')}."
        embed.add_field(name="How do I use this bot?", value="Just mention me and start typing! I'll reply to you as soon as I can.")
        embed.add_field(name="How do I reset my session?", value="Just use the `!reset` command. This will reset your session and allow you to start over.")
        embed.add_field(name="Can I add images?", value="Yes! Just attach them to your message.")

        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
        embed.color = discord.Color.blurple()
        
        await ctx.send(embed=embed)

        
async def setup(bot: GeminiBot):
    await bot.add_cog(Chat(bot))

        

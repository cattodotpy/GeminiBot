import discord
from discord.ext import commands
from discord.ui import View, Button
from main import GeminiBot
from helpers.session import Session


class Help(commands.Cog):
    def __init__(self, bot: GeminiBot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title=":gem: Gemini Bot")
        embed.description = f"> Hi, I'm **{self.bot.user.name}**!\n> I'm a chatbot that uses the state-of-the-art Google Gemini AI to chat with you."
        embed.add_field(
            name="How do I use this bot?",
            value="Just mention me and start typing! I'll reply to you as soon as I can. Even with images!",
        )

        embed.set_author(
            name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        )
        embed.set_footer(text="Made with ❤️")
        embed.color = discord.Color.blurple()
        view = View()
        view.add_item(
            Button(label="Support server", url="https://discord.gg/fD56rK2m3W", emoji="👋")
        )
        view.add_item(
            Button(label="GitHub", url="https://github.com/cattodotpy/GeminiBot", emoji="<:Github:1189222428145107024>")
        )
        await ctx.send(embed=embed, view=view)


async def setup(bot: GeminiBot):
    await bot.add_cog(Help(bot))

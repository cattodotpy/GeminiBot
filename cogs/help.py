import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import ButtonStyle
from main import GeminiBot


class HelpView(View):
    def __init__(self, embed: discord.Embed = None, back_view: View = None):
        super().__init__()
        self.embed = embed
        self.back_view = back_view
        self.add_item(
            Button(
                label="Support server",
                url="https://discord.gg/fD56rK2m3W",
                emoji="👋",
                row=2,
            )
        )
        self.add_item(
            Button(
                label="GitHub",
                url="https://github.com/cattodotpy/GeminiBot",
                emoji="<:Github:1189222428145107024>",
                row=2,
            )
        )

    @discord.ui.button(label="Commands", style=ButtonStyle.blurple, row=1)
    async def commands(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.edit_message(embed=self.embed, view=self.back_view)


class BackView(View):
    def __init__(self, embed: discord.Embed = None, help_view: HelpView = None):
        super().__init__()
        self.embed = embed
        self.help_view = help_view
        self.add_item(
            Button(
                label="Support server",
                url="https://discord.gg/fD56rK2m3W",
                emoji="👋",
                row=2,
            )
        )
        self.add_item(
            Button(
                label="GitHub",
                url="https://github.com/cattodotpy/GeminiBot",
                emoji="<:Github:1189222428145107024>",
                row=2,
            )
        )

    @discord.ui.button(label="Back", style=ButtonStyle.danger, row=1)
    async def commands(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.edit_message(
            embed=self.embed, view=self.help_view
        )


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

        comamnds_embed = discord.Embed(title=":gem: Gemini Bot", color=discord.Color.blurple())
        comamnds_embed.description = f"> Hi, I'm **{self.bot.user.name}**!\n> I'm a chatbot that uses the state-of-the-art Google Gemini AI to chat with you."
        comamnds_embed.add_field(
            name="!reset",
            value="Resets your session. This will reset the conversation and the bot will forget everything you've said.",
            inline=False,
        )

        comamnds_embed.add_field(
            name="!delete_last [n]",
            value="Deletes the last `n` message(s) sent by the bot. This will delete the last message sent by the bot, and the bot will forget the last `n` messages you've sent.",
            inline=False,
        )
        comamnds_embed.set_author(
            name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        )

        comamnds_embed.set_footer(text="Made with ❤️")
        back_view = BackView(embed=embed)

        view = HelpView(embed=comamnds_embed)

        view.back_view = back_view
        back_view.help_view = view

        await ctx.send(embed=embed, view=view)


async def setup(bot: GeminiBot):
    await bot.add_cog(Help(bot))

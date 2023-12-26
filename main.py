import json
import logging
import os
import platform
import sys
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)


intents = discord.Intents.all()

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("gemini_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class GeminiBot(commands.Bot):
    def __init__(self, cogs: list[str] = ["cogs.chat", "cogs.help"]) -> None:
        super().__init__(
            command_prefix=config["prefix"],
            intents=intents,
            help_command=None,
        )
        self.logger = logger
        self.config = config
        self.cogs_to_load = cogs

    async def setup_hook(self) -> None:
        """
        Executed after the bot is once ready.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        await self.load_cogs()

    async def on_command_completion(self, context: Context) -> None:
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def load_cogs(self):
        for cog in self.cogs_to_load:
            try:
                await self.load_extension(cog)
            except Exception as e:
                self.logger.error(f"Failed to load cog {cog}: {e}")
                traceback.print_exc()

    async def on_ready(self) -> None:
        print("Ready.")
load_dotenv()

bot = GeminiBot()

def assert_config():
    assert "prefix" in config, "No prefix specified in config.json"
    assert "owner" in config, "No owner specified in config.json"
    assert "blacklist" in config, "No blacklist specified in config.json"
    assert "initial_prompt" in config, "Initial prompt missing in config.json"

def assert_env():
    assert "BOT_TOKEN" in os.environ, "No BOT_TOKEN specified in environment variables"
    assert "GEMINI_API_KEY" in os.environ, "No GEMINI_API_KEY specified in environment variables"

def main():
    assert_config()
    assert_env()
    bot.run(os.environ["BOT_TOKEN"])

if __name__ == "__main__":
    main()
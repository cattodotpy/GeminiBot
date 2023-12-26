from main import GeminiBot
import discord
from helpers.prepare_env import prepare, visualize_dict
import aiohttp
import base64
import os

GEMINI_PRO_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
)
GEMINI_PRO_VISION_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"


async def build_content(prompt: str, role: str, attachments: list[str] = []):
    content = {"role": role, "parts": [{"text": prompt}]}

    if attachments:
        async with aiohttp.ClientSession() as session:
            for attachment in attachments:
                async with session.get(attachment) as resp:
                    content["parts"].append(
                        {
                            "inline_data": {
                                "mime_type": resp.headers["Content-Type"],
                                "data": base64.b64encode(await resp.read()).decode(
                                    "utf-8"
                                ),
                            }
                        }
                    )

    return content


class Session:
    def __init__(
        self,
        bot: GeminiBot,
        provide_environment: bool = True,
        author: discord.User = None,
        channel: discord.TextChannel = None,
        guild: discord.Guild = None,
    ) -> None:
        self.bot = bot
        self.environment = {}
        if provide_environment and author and channel and guild:
            self.environment = prepare(guild, channel, author)

        self.session = None
        self.vision = False
        self.history = []
        self.request_history = []

    async def initialize(self):
        self.session = aiohttp.ClientSession()
        self.history = [
            await build_content(
                "\n".join(self.bot.config["initial_prompt"]).format(
                    self.bot.user.name, self.bot.config.get("owner", "unknown")
                )
                + visualize_dict(self.environment),
                "user",
            ),
            await build_content(
                "I understand. I am a Discord bot, named {self.bot.user.name}. I will not abuse users, and I will not allow users to abuse me.",
                "model",
            ),
        ]
        return self

    async def close(self):
        await self.session.close()
        return self

    async def send(self, message: str, attachments: list[discord.Attachment] = None):
        print(self.history)
        if attachments:
            self.history.append(await build_content(message, "user"))
            data = {"parts": [{"text": message}]}

            for attachment in attachments:
                async with self.session.get(attachment.url) as resp:
                    data["parts"].append(
                        {
                            "inline_data": {
                                "mime_type": resp.headers["Content-Type"],
                                "data": base64.b64encode(await resp.read()).decode(
                                    "utf-8"
                                ),
                            }
                        }
                    )

            async with self.session.post(
                GEMINI_PRO_VISION_URL + "?key=" + os.environ["GEMINI_API_KEY"],
                json={
                    "contents": [
                        data
                    ]
                },
            ) as resp:
                return await self.resolve_response(resp)
        else:
            self.history.append(await build_content(message, "user"))

            async with self.session.post(
                GEMINI_PRO_URL + "?key=" + os.environ["GEMINI_API_KEY"],
                json={"contents": self.history},
            ) as resp:
                return await self.resolve_response(resp)

    async def resolve_response(self, response: aiohttp.ClientResponse):
        self.request_history.append(response)
        data = await response.json()
        print(data)
        if response.status != 200:
            self.history.pop()
            base = "An error occured while processing your request. Please try again later."
            if "error" in data:
                base += f" Error: {data['error']['message']}"

            return base
        
        if "candidates" not in data or len(data["candidates"]) == 0:
            self.history.pop()
            feedback = data["promptFeedback"]
            text = ""
            text += f"Your request was blocked by the model.\n"
            if reason := feedback.get("blockReason", None):
                text += f"Reason: {reason}\n"

            text+="\nSafety Ratings:"
            for rating in feedback["safetyRatings"]:
                text += f"\n{rating['category']}: {rating['probability'].title()}"

            return text

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        self.history.append(
            await build_content(text, "model")
        )

        return text

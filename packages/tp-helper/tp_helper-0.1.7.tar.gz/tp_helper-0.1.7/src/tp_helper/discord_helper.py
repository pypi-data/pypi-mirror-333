import logging
import aiohttp


class DiscordHelper:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.description = None
        self.color = None
        self.notify_everyone = False

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_colour(self, colour):
        self.color = colour

    def set_notify_everyone(self, notify_everyone):
        self.notify_everyone = notify_everyone

    async def send_error(self, error, desc: str = None):
        self.title = "[Error]"
        self.description = desc
        self.color = "16711680"
        await self._send_message(f"```{error}```")

    async def send_warning(self, warning, desc: str = None):
        self.title = "[Warning]"
        self.description = desc
        self.color = "16746496"
        await self._send_message(f"```{warning}```")

    async def send_info(self, info, desc: str = None):
        self.title = "[Info]"
        self.description = desc
        self.color = "65280"
        await self._send_message(f"```{info}```")

    async def _send_message(self, message: str):
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    self.url,
                    json={
                        "content": f"{"@everyone "if self.notify_everyone else ""}{message}",
                        "tts": False,
                        "username": "Система уведомлений",
                        "embeds": [
                            {
                                "title": self.title,
                                "description": self.description,
                                "color": self.color
                            }
                        ],
                    },
                )
                if response.status != 204:
                    logging.warn(
                        f"Non-204 response from Discord! Response: {await response.text()}"
                    )
        except Exception as e:
            logging.error(f"Could not send message to Discord: {e}")

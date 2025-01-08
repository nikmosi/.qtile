from base64 import b64encode
from typing import override

from httpx import HTTPStatusError
from libqtile.widget.base import InLoopPollText
from loguru import logger

from settings import font_awesome_bold
from settings import conf


class WakaTime(InLoopPollText):
    def __init__(self, token: str, text: str = "", **config):
        super().__init__(text, **config)
        self.token = b64encode(token.encode("ascii")).decode("ascii")
        self.icon = font_awesome_bold.format("")

    @override
    async def poll(self) -> str:  # pyright: ignore
        logger.debug("wakatime poll")
        ans = await conf.net.session.get(
            "https://wakatime.com/api/v1/users/current/status_bar/today",
            headers={"Authorization": f"Basic {self.token}"},
        )
        try:
            ans.raise_for_status()
        except HTTPStatusError as e:
            logger.warning("HttpStatusError from wakatime")
            logger.error(e)
            return "N/A"

        data = ans.json()
        wakatime_today: str = data["data"]["grand_total"]["text"]
        if wakatime_today.isspace():
            return self.icon
        return f"{self.icon} {wakatime_today}"

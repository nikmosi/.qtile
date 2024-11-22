from base64 import b64encode
from http import HTTPStatus

import requests
from libqtile.widget.base import ThreadPoolText
from loguru import logger

from settings import font_awesome_bold


class WakaTime(ThreadPoolText):
    def __init__(self, token: str, text: str = "", **config):
        super().__init__(text, **config)
        self.token = b64encode(token.encode("ascii")).decode("ascii")
        self.icon = font_awesome_bold.format("")

    def poll(self) -> str:
        ans = requests.get(
            "https://wakatime.com/api/v1/users/current/status_bar/today",
            headers={"Authorization": f"Basic {self.token}"},
        )
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            return self.icon
        data = ans.json()
        wakatime_today: str = data["data"]["grand_total"]["text"]
        if wakatime_today.isspace():
            return self.icon
        return f"{self.icon} {wakatime_today}"

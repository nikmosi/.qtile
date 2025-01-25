from base64 import b64encode
from typing import override

from httpx import ConnectError, HTTPStatusError, TimeoutException
from libqtile.widget.base import ThreadPoolText
from loguru import logger

from settings import conf, font_awesome_bold


class WakaTime(ThreadPoolText):
    def __init__(self, token: str, text: str = "", **config):
        super().__init__(text, **config)
        self.token = b64encode(token.encode("ascii")).decode("ascii")
        self.icon = font_awesome_bold.format("")

    @override
    def poll(self) -> str:  # pyright: ignore
        logger.debug("wakatime poll")
        try:
            ans = conf.net.session.get(
                "https://wakatime.com/api/v1/users/current/status_bar/today",
                headers={"Authorization": f"Basic {self.token}"},
            )
            ans.raise_for_status()
        except HTTPStatusError as e:
            logger.warning("HttpStatusError from wakatime")
            logger.error(e)
            return "N/A"
        except ConnectError as e:
            logger.warning("Cant connect")
            logger.error(e)
            return "N/C"
        except TimeoutException as e:
            logger.warning("Timeout")
            logger.error(e)
            return "T/O"

        data = ans.json()
        wakatime_today: str = data["data"]["grand_total"]["text"]
        if wakatime_today.isspace():
            return self.icon
        return f"{self.icon} {wakatime_today}"

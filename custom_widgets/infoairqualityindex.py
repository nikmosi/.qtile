import re
from abc import ABC, abstractmethod
from typing import override

from httpx import ConnectError, HTTPStatusError, Response, TimeoutException

from settings import AirqConfig, conf
from libqtile.widget.base import ThreadPoolText
from loguru import logger
from yarl import URL

from custom_widgets.exceptions.infoairqualityindex import ApiReject
from settings import InfoAirQualityColors
from utils import formats


class AqiGetter(ABC):
    """Aqi - air quality index"""

    url: str = ""

    def request(self) -> Response | None:
        ans = None
        try:
            ans = conf.net.session.get(self.url)
            ans.raise_for_status()
        except HTTPStatusError as e:
            logger.warning("get HttpStatusError from {self.url=}.")
            raise ApiReject from e
        except ConnectError as e:
            logger.warning("Cant connect")
            logger.error(e)
        except TimeoutException as e:
            logger.warning("Timeout")
            logger.error(e)

        return ans

    @abstractmethod
    def get(self) -> int:
        raise NotImplementedError()


class IqAirCurl(AqiGetter):
    def __init__(self, url: URL) -> None:
        self.url = str(url)

    @override
    def get(self) -> int:
        ans = self.request()
        if not ans:
            return -1
        pattern = r"<p class=\"aqi-value__value\">(\d+)\*</p>"
        if match := re.search(pattern, ans.text):
            aqi = match.group(1)
        else:
            aqi = -1
        return int(aqi)


class AqiApi(AqiGetter):
    def __init__(self, aqi_conf: AirqConfig = AirqConfig()):
        api = aqi_conf.api
        city = aqi_conf.city
        token = aqi_conf.token
        self.url = f"{api}/{city}/?token={token}"

    @override
    def get(self) -> int:
        ans = self.request()
        if not ans:
            return -1
        data = ans.json()
        status = data["status"]
        if status != "ok":
            logger.error(f"get {status=}")
            raise ApiReject()
        aqi = data["data"]["aqi"]
        return aqi


class InfoAirQualitiIndex(ThreadPoolText):
    def __init__(
        self,
        aqi_getter: AqiGetter,
        text: str = "",
        colors=InfoAirQualityColors(),
        **config,
    ):
        super().__init__(text, **config)
        self.aqi_getter = aqi_getter
        self.colors = colors

    def poll(self) -> str:  # pyright: ignore
        res = """<span foreground="{color}" weight="bold">\uea35</span> {value}"""
        try:
            aqi = self.aqi_getter.get()
        except ApiReject:
            return res.format(color=self.colors.red, value="=")
        else:
            padded_aqi = formats.ljust_with_disabled_zero(2, str(aqi))
            if aqi < 50:
                return res.format(color=self.colors.green, value=padded_aqi)
            elif aqi < 100:
                return res.format(color=self.colors.yellow, value=padded_aqi)
            elif aqi < 150:
                return res.format(color=self.colors.orange, value=padded_aqi)
            elif aqi < 200:
                return res.format(color=self.colors.pink, value=padded_aqi)
            elif aqi < 300:
                return res.format(color=self.colors.purple, value=padded_aqi)
            return res.format(color=self.colors.red, value=padded_aqi)

import re
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import override

import requests
from libqtile.widget.base import ThreadPoolText
from loguru import logger
from yarl import URL

from custom_widgets.exceptions.infoairqualityindex import ApiReject
from settings import InfoAirQualityColors
from utils import formats


class AqiGetter(ABC):
    """Aqi - air quality index"""

    @abstractmethod
    def get(self) -> int:
        raise NotImplementedError()


class IqAirCurl(AqiGetter):
    def __init__(self, url: URL) -> None:
        self._url = str(url)

    @override
    def get(self) -> int:
        ans = requests.get(self._url)
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self._url}")
            raise ApiReject()
        pattern = r"<p class=\"aqi-value__value\">(\d+)\*</p>"
        if match := re.search(pattern, ans.text):
            aqi = match.group(1)
        else:
            aqi = -1
        return int(aqi)


class AqiApi(AqiGetter):
    def __init__(self, token, city, api):
        self.url = f"{api}/{city}/?token={token}"

    @override
    def get(self) -> int:
        ans = requests.get(self.url)
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            raise ApiReject()
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
        colors=InfoAirQualityColors,
        **config,
    ):
        super().__init__(text, **config)
        self.aqi_getter = aqi_getter
        self._colors = InfoAirQualityColors

    def poll(self) -> str:
        res = """<span foreground="{color}" weight="bold">\uea35</span> {value}"""
        try:
            aqi = self.aqi_getter.get()
        except ApiReject:
            return res.format(color=self._colors.red, value="=")
        else:
            padded_aqi = formats.ljust_with_disabled_zero(2, str(aqi))
            if aqi < 50:
                return res.format(color=self._colors.green, value=padded_aqi)
            elif aqi < 100:
                return res.format(color=self._colors.yellow, value=padded_aqi)
            elif aqi < 150:
                return res.format(color=self._colors.orange, value=padded_aqi)
            elif aqi < 200:
                return res.format(color=self._colors.pink, value=padded_aqi)
            elif aqi < 300:
                return res.format(color=self._colors.purple, value=padded_aqi)
            return res.format(color=self._colors.red, value=padded_aqi)

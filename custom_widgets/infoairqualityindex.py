import re
from abc import ABC, abstractmethod
from http import HTTPStatus

import requests
from libqtile.widget.base import ThreadPoolText
from loguru import logger

from utils import formats


class AqiGetter(ABC):
    @abstractmethod
    def get(self) -> int:
        raise NotImplementedError()


class IqAirCurl(AqiGetter):
    def get(self) -> int:
        url = "https://www.iqair.com/russia/novosibirsk"
        ans = requests.get(url)
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {url}")
            raise IOError()
        pattern = r"<p class=\"aqi-value__value\">(\d+)\*</p>"
        try:
            aqi = re.search(pattern, ans.text).group(1)
        except IndexError:
            aqi = -1
        return int(aqi)


class AqiApi(AqiGetter):
    def __init__(self, token, city, api):
        self.url = f"{api}/{city}/?token={token}"

    def get(self) -> int:
        ans = requests.get(self.url)
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            raise IOError()
        data = ans.json()
        status = data["status"]
        if status != "ok":
            logger.error(f"get {status=}")
            raise IOError()
        aqi = data["data"]["aqi"]
        return aqi


class InfoAirQualitiIndex(ThreadPoolText):
    class Colors:
        green = "#009966"
        yellow = "#ffde33"
        orange = "#ff9933"
        pink = "#cc0033"
        purple = "#660099"
        red = "#7e0023"

    def __init__(self, aqi_getter: AqiGetter, text: str = "", **config):
        super().__init__(text, **config)
        self.aqi_getter = aqi_getter

    def poll(self):
        res = """<span foreground="{color}" weight="bold">\uea35</span> {value}"""
        try:
            aqi = self.aqi_getter.get()
        except IOError:
            return res.format(color=self.Colors.red, value="=")
        else:
            padded_aqi = formats.ljust_with_disabled_zero(2, str(aqi))
            if aqi < 50:
                return res.format(color=self.Colors.green, value=padded_aqi)
            elif aqi < 100:
                return res.format(color=self.Colors.yellow, value=padded_aqi)
            elif aqi < 150:
                return res.format(color=self.Colors.orange, value=padded_aqi)
            elif aqi < 200:
                return res.format(color=self.Colors.pink, value=padded_aqi)
            elif aqi < 300:
                return res.format(color=self.Colors.purple, value=padded_aqi)
        return res.format(color=self.Colors.red, value=padded_aqi)

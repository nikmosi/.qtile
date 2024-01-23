import datetime
import json
from http import HTTPStatus

import requests
from libqtile.widget.base import ThreadPoolText
from loguru import logger


class InfoAirQualitiIndex(ThreadPoolText):
    class Colors:
        green = "#009966"
        yellow = "#ffde33"
        orange = "#ff9933"
        pink = "#cc0033"
        purple = "#660099"
        red = "#7e0023"

    def __init__(self, token, city, api, text="", **config):
        super().__init__(text, **config)
        self.url = f"{api}/{city}/?token={token}"

    def poll(self):
        datetime.datetime.now().time().__str__()
        ans = requests.get(self.url)
        res = """<span foreground="{color}" weight="bold">\uea35</span> {value}"""
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            return res.format(color=self.Colors.red, value="=")
        data = json.loads(ans.text)
        status = data["status"]
        if status != "ok":
            logger.error(f"get {status=}")
            return res.format(color=self.Colors.red, value="=")
        aqi = data["data"]["aqi"]
        if aqi < 50:
            return res.format(color=self.Colors.green, value=aqi)
        elif aqi < 100:
            return res.format(color=self.Colors.yellow, value=aqi)
        elif aqi < 150:
            return res.format(color=self.Colors.orange, value=aqi)
        elif aqi < 200:
            return res.format(color=self.Colors.pink, value=aqi)
        elif aqi < 300:
            return res.format(color=self.Colors.purple, value=aqi)
        return res.format(color=self.Colors.red, value=aqi)

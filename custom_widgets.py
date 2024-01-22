import datetime
import json
from base64 import b64encode
from http import HTTPStatus
from typing import Literal

import requests
from libqtile import widget
from libqtile.lazy import lazy
from libqtile.widget.base import ThreadPoolText
from loguru import logger


class NextFormatsClock(widget.Clock):
    def __init__(self, formats: list, *args, **kwargs):
        self.formats = formats
        self.format_index = 0
        super().__init__(format=formats[self.format_index], *args, **kwargs)
        if "Button1" in self.mouse_callbacks:
            self.mouse_callbacks["Button1"] = self.combine(
                [self.click_func(), self.mouse_callbacks["Button1"]]
            )
        else:
            self.mouse_callbacks["Button1"] = self.click_func()

    def combine(self, funcs: list):
        @lazy.function
        def executor(qtile):
            print("execurot")
            print(len(funcs))
            for i in funcs:
                qtile.server.call((i.selectors, i.name, i.args, i.kwargs))

        return executor

    def click_func(self):
        @lazy.function
        def next_clock_fomat(_):
            print("format")
            self.format_index += 1
            self.format_index %= len(self.formats)
            self.format = self.formats[self.format_index]
            self.update(self.poll())

        return next_clock_fomat


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


class WakaTime(ThreadPoolText):
    def __init__(self, token: str, text: str = "", **config):
        super().__init__(text, **config)
        self.token = b64encode(token.encode("ascii")).decode("ascii")

    def poll(self):
        ans = requests.get(
            "https://wakatime.com/api/v1/users/current/status_bar/today",
            headers={"Authorization": f"Basic {self.token}"},
        )
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            return ""
        data = json.loads(ans.text)
        wakatime_today: str = data["data"]["grand_total"]["text"]
        return "" if wakatime_today.isspace() else f" {wakatime_today}"


class OpenWeatherMap(ThreadPoolText):
    def __init__(self, api, key, city_id, units="metric", text="", **config):
        super().__init__(text, **config)
        self.url = f"{api}/weather?appid={key}&id={city_id}&units={units}"

    def get_weather_icons_font(self, weather_icon):
        match weather_icon:
            case "01d":
                icon = ""
            case "01n":
                icon = ""
            case "02d":
                icon = ""
            case "02n":
                icon = ""
            case "03d" | "03n":
                icon = ""
            case "04d" | "04n":
                icon = ""
            case "09d":
                icon = ""
            case "09n":
                icon = ""
            case "10d":
                icon = ""
            case "10n":
                icon = ""
            case "11d":
                icon = ""
            case "11n":
                icon = ""
            case "13d":
                icon = ""
            case "13n":
                icon = ""
            case "50d":
                icon = ""
            case "50n":
                icon = ""
            case _:
                icon = ""
        return icon

    def get_font_awesome_5_pro_icon(self, weather_icon):
        match weather_icon:
            case "01d":
                icon = ""
            case "01n":
                icon = ""
            case "02d":
                icon = ""
            case "02n":
                icon = ""
            case "03d":
                icon = ""
            case "03n":
                icon = ""
            case "04*":
                icon = ""
            case "09*":
                icon = ""
            case "10d":
                icon = ""
            case "10n":
                icon = ""
            case "11*":
                icon = ""
            case "13*":
                icon = ""
            case "50*":
                icon = ""
            case _:
                icon = ""
        return icon

    def get_icon(self, weather_icon, font: Literal["weather", "awesome"] = "weather"):
        match font:
            case "weather":
                return self.get_weather_icons_font(weather_icon)
            case "awesome":
                return self.get_font_awesome_5_pro_icon(weather_icon)

    def poll(self):
        ans = requests.get(self.url)
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            return ""
        data = json.loads(ans.text)

        weather_desc = data["weather"][0]["description"]
        weather_temp = int(data["main"]["temp"])
        weather_icon = data["weather"][0]["icon"]

        symbol = "°"
        icon_formatting = """<span font_family="Weather Icons">{}</span>"""
        icon = icon_formatting.format(self.get_icon(weather_icon))
        return f"{icon} {weather_desc} {weather_temp}{symbol}"

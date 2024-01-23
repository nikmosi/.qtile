import json
from http import HTTPStatus
from typing import Literal

import requests
from libqtile.widget.base import ThreadPoolText
from loguru import logger


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

from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import override

import requests
from libqtile.widget.base import ThreadPoolText
from loguru import logger


class IconProvider(ABC):
    @abstractmethod
    def get_icon(self, weather_icon: str) -> str:
        """
        By code of icon return unicode icon
        """
        raise NotImplementedError


class OpenWeatherMap(ThreadPoolText):
    def __init__(
        self,
        api,
        key,
        city_id,
        icon_provider: IconProvider | None = None,
        units="metric",
        text="",
        **config,
    ):
        super().__init__(text, **config)
        self.url = f"{api}/weather?appid={key}&id={city_id}&units={units}"
        self.icon_provider = icon_provider if icon_provider else FontAwesome5Pro()

    def get_icon(self, weather_icon):
        return self.icon_provider.get_icon(weather_icon)

    def poll(self):
        ans = requests.get(self.url)
        if ans.status_code != HTTPStatus.OK:
            logger.error(f"didn't get and from {self.url}")
            return ""
        data = ans.json()

        weather_desc = data["weather"][0]["description"]
        weather_temp = int(data["main"]["temp"])
        weather_icon = data["weather"][0]["icon"]

        symbol = "°"
        icon_formatting = """<span font_family="Weather Icons">{}</span>"""
        icon = icon_formatting.format(self.get_icon(weather_icon))
        return f"{icon} {weather_desc} {weather_temp}{symbol}"


class WeatherIcon(IconProvider):
    @override
    def get_icon(self, weather_icon: str) -> str:
        icon_map = {
            "01d": "",
            "01n": "",
            "02d": "",
            "02n": "",
            "03d": "",
            "03n": "",
            "04d": "",
            "04n": "",
            "09d": "",
            "09n": "",
            "10d": "",
            "10n": "",
            "11d": "",
            "11n": "",
            "13d": "",
            "13n": "",
            "50d": "",
            "50n": "",
        }
        default_icon = ""
        return icon_map.get(weather_icon, default_icon)


class FontAwesome5Pro(IconProvider):
    @override
    def get_icon(self, weather_icon: str) -> str:
        icon_map = {
            "01d": "",
            "01n": "",
            "02d": "",
            "02n": "",
            "03d": "",
            "03n": "",
            "04n": "",
            "04d": "",
            "09n": "",
            "09d": "",
            "10d": "",
            "10n": "",
            "11n": "",
            "11d": "",
            "13n": "",
            "13d": "",
            "50n": "",
            "50d": "",
        }
        default_icon = ""
        return icon_map.get(weather_icon, default_icon)

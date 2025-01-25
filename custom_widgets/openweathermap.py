from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override

from httpx import ConnectError, HTTPStatusError, TimeoutException
from libqtile.widget.base import ThreadPoolText
from loguru import logger

from settings import OpenWeatherConfig, conf


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
        weather_conf=OpenWeatherConfig(),
        icon_provider: IconProvider | None = None,
        units="metric",
        text="",
        **config,
    ):
        super().__init__(text, **config)
        api = weather_conf.api
        key = weather_conf.key
        city_id = weather_conf.city
        self.icon_format = "" """<span font_family="Weather Icons">{}</span>"""
        self.url = f"{api}/weather?appid={key}&id={city_id}&units={units}"
        self.icon_provider = icon_provider if icon_provider else WeatherIcon()

    def get_icon(self, weather_icon) -> str:
        icon = self.icon_provider.get_icon(weather_icon)
        return self.icon_format.format(icon)

    def poll(self) -> str:  # pyright: ignore
        logger.debug(f"get weather from {self.url}")
        ans = conf.net.session.get(self.url)
        try:
            ans.raise_for_status()
        except HTTPStatusError as e:
            logger.warning(f"didn't get and from {self.url}")
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

        weather_desc = data["weather"][0]["description"]
        weather_temp = int(data["main"]["temp"])
        weather_icon = data["weather"][0]["icon"]

        symbol = "°"
        icon = self.get_icon(weather_icon)
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

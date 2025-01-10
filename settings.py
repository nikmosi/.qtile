from functools import cached_property
import os
from os import path
from pathlib import Path

from dotenv import load_dotenv
from libqtile import widget
from pydantic import BaseModel, ConfigDict, Field
from httpx import Client
from loguru import logger

base_path = os.path.dirname(__file__)
dotenv_path = os.path.join(base_path, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logger.add(Path.home() / ".local" / "share" / "qtile" / "loguru.log", level="DEBUG")
logger.info("_____________ start _____________ ")


class InfoAirQualityColors:
    green = "#009966"
    yellow = "#ffde33"
    orange = "#ff9933"
    pink = "#cc0033"
    purple = "#660099"
    red = "#7e0023"


class Colors:
    background = "#282A2E"
    background_alt = "#373B41"
    foreground = "#C5C8C6"
    primary = "#F0C674"
    secondary = "#8ABEB7"
    alert = "#A54242"
    disabled = "#707880"


class NetConfig(BaseModel):
    session: Client = Field(default_factory=lambda: Client(timeout=3))

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BaseColorsConfig(BaseModel):
    main: Colors = Colors()
    air_quality: InfoAirQualityColors = InfoAirQualityColors()

    model_config = ConfigDict(arbitrary_types_allowed=True)


class FormatsConfig(BaseModel):
    disabled_text: str = f"<span foreground='{Colors.disabled}'>{{text}}</span>"

    @cached_property
    def disabled_zero_pad(self) -> str:
        return self.disabled_text.format(text="0")


class ImgurConfig(BaseModel):
    client_id: str = os.getenv("IMGUR_CLIENT_ID")
    url: str = "https://api.imgur.com/3/image"


class AirqConfig(BaseModel):
    token: str = os.getenv("INFO_AIRQUALITYINDEX_TOKEN")
    city: str = os.getenv("INFO_AIRQUALITYINDEX_CITY")
    api: str = os.getenv("INFO_AIRQUALITYINDEX_API")


class OpenWeatherConfig(BaseModel):
    key: str = os.getenv("OPENWEATHERMAP_KEY")
    city: str = os.getenv("OPENWEATHERMAP_CITY")
    api: str = os.getenv("OPENWEATHERMAP_API")


class WakatimeConfig(BaseModel):
    token: str = os.getenv("WAKATIME_TOKEN", "")


class Config(BaseModel):
    net: NetConfig = Field(default_factory=NetConfig)
    home: Path = Field(default_factory=lambda: Path.home())
    formats: FormatsConfig = Field(default_factory=FormatsConfig)
    imgur: ImgurConfig = Field(default_factory=ImgurConfig)
    airq: AirqConfig = Field(default_factory=AirqConfig)
    weather: OpenWeatherConfig = Field(default_factory=OpenWeatherConfig)
    waka: WakatimeConfig = Field(default_factory=WakatimeConfig)

    model_config = ConfigDict(arbitrary_types_allowed=True)


conf = Config()


home = Path.home()

wallpaper_path = path.join(home, "Pictures", "wallpaper")

wallpaper_screen_1 = path.join(wallpaper_path, "1")
wallpaper_screen_2 = path.join(wallpaper_path, "2")


font_template = f"<span foreground='{Colors.primary}' \
        font_family='{{font_family}}' weight='{{weight}}'>{{text}}</span>"
font_awesome_bold = font_template.format(
    font_family="FontAwesome6Pro", weight="bold", text="{}"
)
font_awesome_brands_bold = font_template.format(
    font_family="FontAwesome6Brands", weight="bold", text="{}"
)

mod = "mod4"
terminal = "alacritty"

pass_clip = path.join(home, "Applications", "pass-clip-helper.sh")
password_selector = (
    "alacritty --title fzf-passwordstore --class float_pass -e" + pass_clip
)

pass_tessen = path.join(home, "Applications", "pass-tessen-helper.sh")
password_manager = (
    "alacritty --title fzf-passwordstore --class float_pass -e " + pass_tessen
)

rofi_theme = "  "
rofi_command = f"rofi -show drun {rofi_theme}"


clipboard_selector = (
    "rofi -modi \"clipboard:greenclip print\" -show clipboard -run-command '{cmd}' "
    + rofi_theme
)

clock_formats = [
    font_awesome_bold.format("  ") + "%I:%M %p",
    font_awesome_bold.format("  ") + "%a, %d %b %Y",
]
block = "{}"
separator = widget.TextBox(
    " ", foreground=Colors.disabled, background=Colors.background, fmt="{}"
)

maim_command = "maim {args}"
xclip_image = "xclip -selection clipboard -t image/png {path}"
xclip_text = "echo -n '{text}' | xclip -sel clip"

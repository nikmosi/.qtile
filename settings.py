# type: ignore
import os
from functools import cached_property
from os import path
from pathlib import Path

from dotenv import load_dotenv
from httpx import Client
from libqtile import widget
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field

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
    background = "#1a1b26"
    background_alt = "#373B41"
    foreground = "#c0caf5"
    primary = "#7aa2f7"
    secondary = "#8ABEB7"
    alert = "#f7768e"
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
    url: str = "https://i.nuuls.com/upload"


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
    font_family="Font Awesome 6 Pro", weight="bold", text="{}"
)
font_awesome_brands_bold = font_template.format(
    font_family="FontAwesome 6 Brands", weight="bold", text="{}"
)

mod = "mod4"
terminal = "kitty"

pass_clip = path.join(home, "Applications", "pass-clip-helper.sh")
password_selector = (
    "alacritty --title fzf-passwordstore --class float_pass -e" + pass_clip
)

password_manager = "rofi-pass"

rofi_theme = "  "
rofi_command = f"rofi -show drun {rofi_theme}"
rofi_power_menu = """rofi -show p \
-modi p:'rofi-power-menu --symbols-font "Symbols Nerd Font Mono"' \
-font "JetBrains Mono NF 16" \
-theme-str 'window {width: 8em;} listview {lines: 6;}'"""


clipboard_selector = "env CM_LAUNCHER=rofi clipmenu -l rofi"

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

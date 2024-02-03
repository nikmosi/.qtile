import os

from dotenv import load_dotenv
from libqtile import widget
from loguru import logger


class Colors:
    background = "#282A2E"
    background_alt = "#373B41"
    foreground = "#C5C8C6"
    primary = "#F0C674"
    secondary = "#8ABEB7"
    alert = "#A54242"
    disabled = "#707880"


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


font_template = "<span foreground='#F0C674' \
        font_family='{font_family}' weight='{weight}'>{text}</span>"
font_awesome_bold = font_template.format(
    font_family="FontAwesome6Pro", weight="bold", text="{}"
)
font_awesome_brands_bold = font_template.format(
    font_family="FontAwesome6Brands", weight="bold", text="{}"
)

home = os.path.expanduser("~")
mod = "mod4"
alt = "mod1"
terminal = "alacritty"
rofi_bash = home + "/.config/rofi/launcher/launcher.sh"

pass_clip = f"{home}/Applications/pass-clip-helper.sh"
password_selector = (
    "alacritty --title fzf-passwordstore --class float_pass -e" + pass_clip
)

pass_tessen = f"{home}/Applications/pass-tessen-helper.sh"
password_manager = (
    "alacritty --title fzf-passwordstore --class float_pass -e " + pass_tessen
)


clipboard_selector = (
    "rofi -modi \"clipboard:greenclip print\" -show clipboard -run-command '{cmd}' "
    + f" -theme {home}/.config/rofi/launcher/style-5.rasi"
)

scrot_command = (
    "scrot '/tmp/%F_%T_$wx$h.png' "
    + "-e 'xclip -selection clipboard -target image/png -i $f' "
    + "{args}"
)

clock_formats = [
    font_awesome_bold.format("  ") + "%I:%M %p",
    font_awesome_bold.format("  ") + "%a, %d %b %Y",
]
block = "[ {} ]"
separator = widget.TextBox("┇", foreground=Colors.disabled)

airq_token = os.getenv("INFO_AIRQUALITYINDEX_TOKEN")
airq_city = os.getenv("INFO_AIRQUALITYINDEX_CITY")
airq_api = os.getenv("INFO_AIRQUALITYINDEX_API")

openweather_key = os.getenv("OPENWEATHERMAP_KEY")
openweather_city = os.getenv("OPENWEATHERMAP_CITY")
openweather_api = os.getenv("OPENWEATHERMA_API")

wakatime_token = os.getenv("WAKATIME_TOKEN", default="")
if not wakatime_token:
    err = "wakatime_token is none"
    logger.error(err)
    raise Exception(err)

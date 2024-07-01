import os

from dotenv import load_dotenv
from libqtile import widget
from loguru import logger


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


# class Colors:
#     background = "#13100f"
#     background_alt = "#373B41"
#     foreground = "#f0eae4"
#     primary = "#CE9987"
#     secondary = "#5697C3"
#     alert = "#A54242"
#     disabled = "#a8a39f"


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
terminal = "alacritty"

pass_clip = f"{home}/Applications/pass-clip-helper.sh"
password_selector = (
    "alacritty --title fzf-passwordstore --class float_pass -e" + pass_clip
)

pass_tessen = f"{home}/Applications/pass-tessen-helper.sh"
password_manager = (
    "alacritty --title fzf-passwordstore --class float_pass -e " + pass_tessen
)

rofi_theme = " -theme gruvbox-dark "
rofi_command = home + "/.config/rofi/launcher.sh"


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

airq_token = os.getenv("INFO_AIRQUALITYINDEX_TOKEN")
airq_city = os.getenv("INFO_AIRQUALITYINDEX_CITY")
airq_api = os.getenv("INFO_AIRQUALITYINDEX_API")

openweather_key = os.getenv("OPENWEATHERMAP_KEY")
openweather_city = os.getenv("OPENWEATHERMAP_CITY")
openweather_api = os.getenv("OPENWEATHERMA_API")
client_id = os.getenv("IMGUR_CLIENT_ID")

wakatime_token = os.getenv("WAKATIME_TOKEN", default="")
if not wakatime_token:
    err = "wakatime_token is none"
    logger.error(err)
    raise Exception(err)

disabled_text = f"<span foreground='{Colors.disabled}'>{{text}}</span>"
disabled_zero_pad = disabled_text.format(text="0")

imgur_curl = f"""
curl --location 'https://api.imgur.com/3/image' \
--header 'Authorization: Client-ID {client_id}' \
--form 'image=@"{{filepath}}"' \
--form 'type="image"' \
--form 'title="screenshot"' \
--form 'description="(:"'
"""

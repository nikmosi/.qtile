import os

from libqtile import widget


class Colors:
    background = "#282A2E"
    background_alt = "#373B41"
    foreground = "#C5C8C6"
    primary = "#F0C674"
    secondary = "#8ABEB7"
    alert = "#A54242"
    disabled = "#707880"


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
clock_formats = [
    font_awesome_bold.format("  ") + "%I:%M %p",
    font_awesome_bold.format("  ") + "%a, %d %b %Y",
]
block = "[ {} ]"
separator = widget.TextBox("┇", foreground=Colors.disabled)

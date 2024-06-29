import json
import subprocess as sb
from pathlib import Path
from typing import Callable

from libqtile.lazy import lazy
from libqtile.utils import send_notification

from settings import home, imgur_curl, maim_command, xclip_image, xclip_text
from utils.cli import call_rofi_dmenu


def get_path() -> Path:
    path = sb.check_output(
        f"echo {home}/Pictures/Screenshots/$(date +%F_%T_)$RANDOM.png",
        shell=True,
        text=True,
    ).strip()
    return Path(path)


def call_screenshot_command(args: str = "") -> Path | None:
    path = get_path()
    command = maim_command.format(args=f"{path} {args}")
    try:
        sb.check_call(command, shell=True)
    except sb.CalledProcessError:
        send_notification("error", "can't take screen")
    else:
        return path


def upload(path: Path) -> str | None:
    try:
        out = sb.check_output(
            imgur_curl.format(filepath=path), text=True, shell=True
        ).strip()
        link = json.loads(out)["data"]["link"]
    except sb.CalledProcessError:
        send_notification("can't upload", "process error")
    except KeyError:
        send_notification("can't upload", "key error")
    else:
        return link


def to_clip(path: Path | None):
    if not path:
        return
    sb.check_call(xclip_image.format(path=path), shell=True)


def get_alternative_screenshot_funcs() -> dict[str, Callable]:
    funcs = [take_full_screenshot, take_screen_and_upload, recongnize_qr]
    return {i.__name__: i for i in funcs}


@lazy.function
def take_screenshot_alternative(_):
    variants = get_alternative_screenshot_funcs()
    rofi_response = call_rofi_dmenu(variants.keys())
    if not rofi_response:
        return
    variants[rofi_response]()


@lazy.function
def take_screenshot(_):
    path = call_screenshot_command(" -s")
    to_clip(path)


def recongnize_qr():
    try:
        sb.check_call(
            "maim -qs | zbarimg -q --raw - | xclip -selection clipboard -f", shell=True
        )
    except sb.CalledProcessError:
        send_notification("error", "can't screenshot")


def take_full_screenshot():
    path = call_screenshot_command()
    to_clip(path)


def take_screen_and_upload():
    path = call_screenshot_command(" -s")
    if not path:
        return
    send_notification("screenshot", "uploading")
    link = upload(path)
    if not link:
        return
    sb.check_call(xclip_text.format(text=link), shell=True)
    send_notification("screenshot", f"link in clip - {link}")

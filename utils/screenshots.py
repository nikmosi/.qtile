import json
import subprocess as sb
from pathlib import Path

from libqtile.lazy import lazy
from libqtile.utils import send_notification

from settings import home, imgur_curl, maim_command, xclip_image, xclip_text


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


@lazy.function
def take_full_screenshot(_):
    path = call_screenshot_command()
    to_clip(path)


@lazy.function
def take_region_screenshot(_):
    path = call_screenshot_command(" -s")
    to_clip(path)


@lazy.function
def take_screen_and_upload(_):
    path = call_screenshot_command(" -s")
    if not path:
        return
    link = upload(path)
    if not link:
        return
    sb.check_call(xclip_text.format(text=link), shell=True)
    send_notification("screenshot", f"link in clip - {link}")

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


def upload(path: Path) -> str:
    out = sb.check_output(
        imgur_curl.format(filepath=path), text=True, shell=True
    ).strip()
    return json.loads(out)["link"]


@lazy.function
def take_full_screenshot(_):
    path = call_screenshot_command()
    sb.check_call(xclip_image.format(path=path), shell=True)


@lazy.function
def take_region_screenshot(_):
    path = call_screenshot_command(" -s")
    sb.check_call(xclip_image.format(path=path), shell=True)


@lazy.function
def take_screen_and_upload(_):
    path = call_screenshot_command(" -s")
    if not path:
        return
    link = upload(path)
    sb.check_call(xclip_text.format(text=link), shell=True)
    send_notification("screenshot", f"link in clip - {link}")

import json
import subprocess as sb
from pathlib import Path

from libqtile.lazy import lazy
from libqtile.utils import send_notification

from settings import client_id, home

scrot_command = (
    f"scrot '{home}/Pictures/Screenshots/%F_%T_$wx$h.png' "
    + " {args} "
    + "-e 'echo $f' "
)

xclip_image = "xclip -selection clipboard -target image/png -i {file}"

xclip_text = "echo -n '{text}' | xclip -sel clip"

imgur_curl = f"""
curl --location 'https://api.imgur.com/3/image' \
--header 'Authorization: Client-ID {client_id}' \
--form 'image=@"{{filepath}}"' \
--form 'type="image"' \
--form 'title="screenshot"' \
--form 'description="(:"'
"""


def call_scrot(args: str = "") -> Path:
    path = sb.check_output(
        scrot_command.format(args=args), text=True, encoding="UTF-8", shell=True
    ).strip()
    return Path(path)


def image_path_to_clip(path: Path) -> None:
    sb.check_call(xclip_image.format(file=path), text=True, shell=True)


def upload(path: Path) -> str:
    out = sb.check_output(
        imgur_curl.format(filepath=path), text=True, shell=True
    ).strip()
    return json.loads(out)["link"]


def text_to_clip(text: str):
    sb.check_call(xclip_text.format(text=text), shell=True)


def take_screenshot(args: str = ""):
    path = call_scrot(args)
    image_path_to_clip(path)
    send_notification("screenshot", "image in clipboard")


@lazy.function
def take_full_screenshot(*args, **kwargs):
    take_screenshot()


@lazy.function
def take_region_screenshot(*args, **kwargs):
    take_screenshot("-s")


@lazy.function
def take_screen_and_upload(*args, **kwargs):
    path = call_scrot("-s")
    link = upload(path)
    text_to_clip(link)
    send_notification("screenshot", f"link in clip - {link}")

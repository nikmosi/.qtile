import subprocess as sb
from pathlib import Path
from typing import Callable

import httpx
from libqtile.lazy import lazy
from libqtile.utils import send_notification
from loguru import logger

from settings import conf, home, maim_command, xclip_image, xclip_text
from utils.cli import call_rofi_dmenu

alternative_screenshot_funcs = []


def alternative_screenshot(func: Callable) -> Callable:
    alternative_screenshot_funcs.append(func)
    return func


def get_path() -> Path:
    path = sb.check_output(
        f"echo {home}/Pictures/screenshots/$(date +%F_%T_)$RANDOM.png",
        shell=True,
        text=True,
    ).strip()
    logger.info(f"Created {path=}.")
    return Path(path)


def call_screenshot_command(args: str = "") -> Path | None:
    path = get_path()
    command = maim_command.format(args=f"{path} {args}")
    logger.debug(f"calling main. {command}")
    try:
        sb.check_call(command, shell=True)
    except sb.CalledProcessError as e:
        msg = "can't take screen"
        logger.warning(msg)
        logger.error(e)
        send_notification("error", msg)
    else:
        return path


def upload(path: Path) -> str | None:
    logger.debug(f"uploding file: {path=}")
    headers = {"Authorization": f"Client-ID {conf.imgur.client_id}"}
    data = {"type": "image", "title": "screenshot", "description": "(:"}
    files = {"image": open(path, "rb")}

    with httpx.Client() as client:
        response = client.post(conf.imgur.url, headers=headers, data=data, files=files)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        msg = f"Upload failed: {response.status_code}, {response.text}"
        logger.warning(msg)
        logger.error(e)
        raise e
    else:
        link = response.json()["data"]["link"]
        return link


def to_clip(path: Path | None) -> None:
    logger.debug("Placing file to clipboard.")
    if not path:
        return
    sb.check_call(xclip_image.format(path=path), shell=True)


def get_alternative_screenshot_funcs() -> dict[str, Callable]:
    return {i.__name__: i for i in alternative_screenshot_funcs}


@lazy.function
def take_screenshot_alternative(_) -> None:
    variants = get_alternative_screenshot_funcs()
    rofi_response = call_rofi_dmenu(variants.keys())
    if not rofi_response:
        logger.warning(f"{rofi_response=} is None.")
        return
    variants[rofi_response]()


@lazy.function
def take_screenshot(_) -> None:
    path = call_screenshot_command(" -s")
    to_clip(path)


@alternative_screenshot
def recongnize_qr() -> None:
    logger.debug("recongnizing qr")
    try:
        sb.check_call(
            "maim -qs | zbarimg -q --raw - | xclip -selection clipboard -f", shell=True
        )
    except sb.CalledProcessError as e:
        msg = "can't screenshot"
        logger.warning(msg)
        logger.error(e)
        send_notification("error", msg)


@alternative_screenshot
def take_full_screenshot():
    logger.debug("taking full screenshot")
    path = call_screenshot_command()
    to_clip(path)


@alternative_screenshot
def take_screen_and_upload():
    logger.debug("taking screenshot and upload")
    path = call_screenshot_command(" -s")
    if not path:
        return
    link = upload(path)
    if not link:
        return
    sb.check_call(xclip_text.format(text=link), shell=True)
    send_notification("screenshot", f"link in clip - {link}")

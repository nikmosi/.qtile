import subprocess as sb
from typing import Iterable

from loguru import logger

from settings import rofi_theme


def call_rofi_dmenu(values: Iterable[str]) -> str | None:
    command = f"rofi -dmenu {rofi_theme}"
    logger.debug(f"calling {command=}")
    try:
        ans = sb.check_output(
            command, shell=True, text=True, input="\n".join(values)
        ).strip()
    except sb.CalledProcessError:
        logger.warning(f"process exit with error. {command}")
    else:
        return ans

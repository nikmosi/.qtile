import subprocess as sb
from typing import Iterable

from libqtile.utils import send_notification

from settings import rofi_theme


def call_rofi_dmenu(values: Iterable[str], sep: str = "|") -> str | None:
    value = sep.join(values)
    command = f'echo "{value}" | rofi -dmenu -sep "{sep}" {rofi_theme}'
    try:
        ans = sb.check_output(command, shell=True, text=True).strip()
    except sb.CalledProcessError:
        send_notification("error", f"problem with {command}")
    else:
        return ans

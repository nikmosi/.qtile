import subprocess as sb
from collections.abc import Sequence

from libqtile.backend.base.window import Window
from libqtile.config import Key, KeyChord
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.utils import send_notification

from settings import (
    clipboard_selector,
    mod,
    password_manager,
    password_selector,
    rofi_command,
    rofi_power_menu,
    terminal,
)
from utils.cli import call_rofi_dmenu
from utils.screenshots import take_screenshot, take_screenshot_alternative


@lazy.function
def prismatik_off_and_poweroff(_):
    send_notification("off", "prismatik", id_=1)
    sb.run(["prismatik", "--off"])
    sb.run(["prismatik", "--off"])
    sb.run(["sleep", "0.4"])
    send_notification("off", "system", id_=2)
    sb.run(["poweroff"])


@lazy.function
def call_rofi_power_menu(_):
    sb.run(rofi_power_menu, shell=True, check=True)


@lazy.function
def change_volume(qtile, increase_vol: bool):
    pulse = qtile.widgets_map.get("pulse_volume")
    if pulse is None:
        send_notification("err", "Pulse volume widget not found")
        return

    volume = pulse.volume
    if increase_vol:
        pulse.increase_vol()
        volume += 2
    else:
        pulse.decrease_vol()
        volume -= 2

    icon = "audio-volume-high"
    message = f"Volume: {volume}%"

    sb.run(
        [
            "notify-send",
            "-u",
            "low",
            "-h",
            f"int:value:{volume}",
            "-h",
            "string:x-dunst-stack-tag:volume",
            message,
            "-i",
            icon,
        ]
    )


@lazy.function
def toggle_minimize_window(qtile: Qtile) -> None:
    windows: Sequence[Window] = qtile.current_group.windows
    names = [f"{i}: {w.name}" for i, w in enumerate(windows)]
    selected_window = call_rofi_dmenu(names)
    if not selected_window:
        return
    id = names.index(selected_window)
    window = windows[id]
    window.toggle_minimize()


keys = [
    Key(["mod1"], "Shift_L", lazy.widget["keyboardlayout"].next_keyboard()),
    Key(["shift"], "Alt_L", lazy.widget["keyboardlayout"].next_keyboard()),
    Key([], "XF86AudioRaiseVolume", change_volume(True)),
    Key([], "XF86AudioLowerVolume", change_volume(False)),
    Key([], "XF86AudioMute", lazy.widget["pulse_volume"].mute()),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "n", toggle_minimize_window, desc="toggle window minimize"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn(rofi_command), desc="Spawn rofi"),
    Key([mod], "p", lazy.spawn(password_selector), desc="Spawn password selector"),
    Key(
        [mod, "shift"], "p", lazy.spawn(password_manager), desc="Spawn password manager"
    ),
    Key([mod], "c", lazy.spawn(clipboard_selector), desc="Spawn clipboard selector"),
    Key(
        [],
        "Print",
        take_screenshot,
        desc="take screenshot",
    ),
    Key(
        ["shift"],
        "Print",
        take_screenshot_alternative,
        desc="take alternative screenshot",
    ),
    Key(
        [mod],
        "x",
        call_rofi_power_menu,
        desc="call rofi power menu",
    ),
]

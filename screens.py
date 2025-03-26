from collections.abc import Sequence

from libqtile import bar, widget
from libqtile.config import Screen
from libqtile.lazy import lazy

from custom_widgets.cGroupBox import GroupBox
from custom_widgets.cSysTray import cSysTray
from custom_widgets.custom_df import CDF
from custom_widgets.infoairqualityindex import AqiApi, InfoAirQualitiIndex
from custom_widgets.kblEmoji import KblEmoji
from custom_widgets.nextformatclock import NextFormatsClock
from custom_widgets.openweathermap import OpenWeatherMap
from custom_widgets.wakatime import WakaTime
from custom_widgets.wireguard import Wireguard
from settings import (
    Colors,
    clock_formats,
    conf,
    font_awesome_bold,
    separator,
    wallpaper_screen_1,
    wallpaper_screen_2,
)
from utils.groups import with_screen_affinity

pulse_volume = widget.PulseVolume(
    name="pulse_volume",
    fmt=font_awesome_bold.format(" ") + "{}",
    mouse_callbacks={
        "Button3": lazy.spawn("pavucontrol -t 3"),
    },
    foreground=Colors.foreground,
)
memory = widget.Memory(
    format=font_awesome_bold.format("  ") + "{MemPercent:_>2.0f}%",
)
cdf = CDF(
    format=font_awesome_bold.format("  ") + "{} Gb",
    update_inteval=60,
)
layout_icon = widget.CurrentLayoutIcon(scale=0.6, padding=10)


def get_screens() -> Sequence[Screen]:
    screens = [
        Screen(
            wallpaper=wallpaper_screen_1,
            wallpaper_mode="fill",
            top=bar.Bar(
                [
                    layout_icon,
                    GroupBox(
                        font="FreeMono, Noto Sans CJK JP",
                        group_filter=with_screen_affinity(0),
                        hide_unused=False,
                        highlight_method="line",
                        inactive=Colors.disabled,
                        this_current_screen_border=Colors.primary,
                        highlight_color=Colors.background_alt,
                        foreground=Colors.primary,
                    ),
                    widget.TextBox(
                        "┇", foreground=Colors.disabled, background=Colors.background
                    ),
                    widget.Prompt(),
                    widget.WindowName(),
                    widget.Chord(
                        chords_colors={
                            "Shutdown": (Colors.alert, Colors.foreground),
                        },
                    ),
                    cSysTray(icon_size=16, ignored_names=["Prismatik"]),
                    separator,
                    Wireguard(update_inteval=3600),
                    separator,
                    widget.CheckUpdates(
                        display_format=font_awesome_bold.format("\uf2f9")
                        + " {updates}",
                        colour_have_updates=Colors.foreground,
                        distro="Arch_yay",
                    ),
                    separator,
                    WakaTime(conf.waka.token, update_inteval=30),
                    separator,
                    OpenWeatherMap(
                        conf.weather,
                        update_inteval=300,
                    ),
                    separator,
                    InfoAirQualitiIndex(
                        AqiApi(conf.airq),
                        update_inteval=300,
                    ),
                    separator,
                    memory,
                    separator,
                    cdf,
                    separator,
                    pulse_volume,
                    separator,
                    NextFormatsClock(formats=clock_formats),
                    separator,
                    KblEmoji(
                        name="keyboardlayout",
                        configured_keyboards=["us", "ru,us"],
                    ),
                    separator,
                ],
                36,
                border_width=[2, 0, 2, 0],
                background=Colors.background,
            ),
        ),
        Screen(
            wallpaper=wallpaper_screen_2,
            wallpaper_mode="fill",
            top=bar.Bar(
                [
                    layout_icon,
                    GroupBox(
                        font="FreeMono, Noto Sans CJK JP",
                        group_filter=with_screen_affinity(1),
                        highlight_method="line",
                        hide_unsed=False,
                        inactive=Colors.disabled,
                        this_current_screen_border=Colors.primary,
                        highlight_color=Colors.background_alt,
                        foreground=Colors.primary,
                    ),
                    separator,
                    widget.Prompt(),
                    widget.Spacer(),
                    separator,
                    NextFormatsClock(formats=clock_formats),
                    separator,
                    separator,
                ],
                32,
                border_width=[2, 0, 2, 0],
                background=Colors.background,
            ),
        ),
    ]
    return screens

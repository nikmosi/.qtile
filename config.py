import subprocess as sb
from dataclasses import dataclass

from libqtile import bar, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.hook import subscribe
from libqtile.layout import columns, floating
from libqtile.layout import max as layoutMax
from libqtile.layout import tile, tree
from libqtile.lazy import lazy

from custom_widgets import InfoAirQualitiIndex, NextFormatsClock, OpenWeatherMap
from keys import keys
from settings import (
    Colors,
    airq_api,
    airq_city,
    airq_token,
    block,
    clock_formats,
    font_awesome_bold,
    home,
    mod,
    openweather_api,
    openweather_city,
    openweather_key,
    separator,
)

# TODO: add
# info-airqualityindex/
# info-wakatime/
# openweathermap-detailed/
# polybar-wireguard/


@dataclass
class ScreenSettings:
    index: int
    key_prefix: str
    group_count: int


@subscribe.client_new
def new_clinet(client):
    if "pavucontrol" in client.get_wm_class():
        client.set_position_floating(2040, 47)
        client.set_size(500, 600)


@subscribe.startup_once
def auto_lunch():
    sb.call([home + "/.config/qtile/scripts/autostart.sh"])


def to_japanese_number(num: int):
    japanese_map = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
    }
    return japanese_map[num]


def get_groups():
    res = []
    for screen in [
        ScreenSettings(index=0, key_prefix="{}", group_count=5),
        ScreenSettings(index=1, key_prefix="F{}", group_count=9),
    ]:
        for i in range(1, screen.group_count + 1):
            group = Group(
                str(len(res) + 1),
                label=str(to_japanese_number(i)),
                screen_affinity=screen.index,
            )
            res.append(group)
            setattr(group, "keycode", screen.key_prefix.format(i))
    firefox_group = Group("", screen_affinity=0, matches=[Match(wm_class="firefox")])
    setattr(firefox_group, "keycode", "w")
    res += [firefox_group]
    return res


groups = get_groups()

for i in groups:
    key = i.keycode
    keys.extend(
        [
            Key(
                [mod],
                key,
                lazy.group[i.name].toscreen(i.screen_affinity),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                key,
                lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    columns.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layoutMax.Max(),
    tile.Tile(border_focus="#881111", border_normal="#220000", border_width=4),
    tree.TreeTab(),
]

widget_defaults = dict(
    font="FreeMono",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def get_groups_name_in_screen(screen_index: int):
    return [i.name for i in groups if i.screen_affinity == screen_index]


screens = [
    Screen(
        wallpaper="/home/nik/Downloads/wallhaven-2yj2px.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.GroupBox(
                    font="FreeMono, Noto Sans CJK JP",
                    visible_groups=get_groups_name_in_screen(0),
                    hide_unused=False,
                    highlight_method="line",
                    inactive=Colors.disabled,
                    this_current_screen_border=Colors.primary,
                    highlight_color=Colors.background_alt,
                    foreground=Colors.primary,
                ),
                separator,
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    fmt=block,
                    chords_colors={
                        "Shutdown": (Colors.alert, Colors.foreground),
                    },
                ),
                widget.Systray(),
                separator,
                OpenWeatherMap(
                    openweather_api, openweather_key, openweather_city, fmt=block
                ),
                separator,
                InfoAirQualitiIndex(airq_token, airq_city, airq_api, fmt=block),
                separator,
                widget.Memory(
                    fmt=block,
                    format=font_awesome_bold.format("  ") + "{MemPercent:.0f}%",
                ),
                separator,
                widget.PulseVolume(
                    fmt=block.format(font_awesome_bold.format(" ") + "{}"),
                    mouse_callbacks={
                        "Button3": lazy.spawn("pavucontrol"),
                    },
                ),
                separator,
                NextFormatsClock(formats=clock_formats, fmt=block),
            ],
            28,
            border_width=[2, 0, 2, 0],
            background=Colors.background,
        ),
    ),
    Screen(
        wallpaper="/home/nik/Downloads/wallhaven-vml95l.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.GroupBox(
                    font="FreeMono, Noto Sans CJK JP",
                    visible_groups=get_groups_name_in_screen(1),
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
                widget.Memory(
                    fmt=block,
                    format=font_awesome_bold.format("  ") + "{MemPercent:.0f}%",
                ),
                separator,
                widget.PulseVolume(
                    fmt=block.format(font_awesome_bold.format(" ") + "{}"),
                    mouse_callbacks={
                        "Button3": lazy.spawn("pavucontrol"),
                    },
                ),
                separator,
                NextFormatsClock(formats=clock_formats, fmt=block),
            ],
            24,
            border_width=[2, 0, 2, 0],
            background=Colors.background,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = floating.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *floating.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="StartWine"),
        Match(wm_class="float_pass"),
        # Match(wm_class="pavucontrol"),
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="BakkesModInjectorCpp"),  # GPG key password entry
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
    ],
    no_reposition_rules=[
        Match(wm_class="pavucontrol"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "bbbb"

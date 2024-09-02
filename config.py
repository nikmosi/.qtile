import re
import subprocess as sb

from libqtile import qtile
from libqtile.config import Click, Drag, Match
from libqtile.hook import subscribe
from libqtile.layout import columns, floating
from libqtile.layout import max as layoutMax
from libqtile.layout import tile, tree
from libqtile.lazy import lazy

from groups import extend_keys, get_groups
from keys import keys
from screens import get_screens
from settings import Colors, block, home, mod


@subscribe.client_new
def new_clinet(client) -> None:
    if "pavucontrol" in client.get_wm_class():
        client.set_position_floating(2040, 47)
        client.set_size(500, 600)


@subscribe.startup_once
def auto_lunch() -> None:
    sb.call([home / ".config/qtile/autostart.sh"])


@subscribe.startup_complete
def complete_hook() -> None:
    qtile.groups_map["firefox"].toscreen(0)
    # qtile.groups_map["chatterino"].toscreen(1)


groups = get_groups()
screens = get_screens()
extend_keys(groups, keys)


layouts = [
    columns.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layoutMax.Max(),
    tile.Tile(border_focus="#881111", border_normal="#220000", border_width=4),
    tree.TreeTab(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono Medium",
    foreground=Colors.foreground,
    fontsize=16,
    padding=3,
    fmt=block,
)
extension_defaults = widget_defaults.copy()

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
dgroups_app_rules = []
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
        Match(wm_class="qbittorrent"),
        Match(wm_class="float_pass"),
        Match(wm_class="floating_wm_class"),
        Match(wm_class="ripdrag"),
        # Match(wm_class="pavucontrol"),
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title=re.compile("^Welcome to .*")),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="BakkesModInjectorCpp"),  # GPG key password entry
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
        Match(wm_class="pinentry-gtk"),  # GPG key password entry
        Match(wm_class="MultiMC"),  # GPG key password entry
    ],
    no_reposition_rules=[
        Match(wm_class="pavucontrol"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "🚀 Blazing 🚀 Fast 🚀 Qtile 🚀"

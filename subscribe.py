import subprocess as sb

from libqtile import qtile
from libqtile.hook import subscribe

from settings import home


@subscribe.client_new
def new_clinet(client) -> None:
    if "pavucontrol" in client.get_wm_class():
        client.set_position_floating(2040, 47)
        client.set_size(500, 600)
    if "nekoray" in client.get_wm_class():
        client.togroup("scratchpad")


@subscribe.startup_once
def auto_lunch() -> None:
    sb.call([home / ".config/qtile/autostart.sh"])


@subscribe.startup_complete
def complete_hook() -> None:
    qtile.groups_map["firefox"].toscreen(0)
    # qtile.groups_map["chatterino"].toscreen(1)

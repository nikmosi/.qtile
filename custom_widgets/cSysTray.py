from collections.abc import Sequence
from libqtile import widget
from libqtile.backend.x11 import window
from libqtile.widget.systray import Icon
from xcffib.xproto import SetMode


class cSysTray(widget.Systray):
    def __init__(self, ignored_names: Sequence = (), *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ignored_names = list(ignored_names)

    def handle_ClientMessage(self, event):
        atoms = self.conn.atoms

        opcode = event.type
        data = event.data.data32
        message = data[1]
        wid = data[2]

        parent = self.bar.window.window

        if opcode == atoms["_NET_SYSTEM_TRAY_OPCODE"] and message == 0:
            w = window.XWindow(self.conn, wid)
            icon = Icon(w, self.qtile, self)
            if icon not in self.tray_icons and icon.name not in self.ignored_names:
                self.tray_icons.append(icon)
                self.tray_icons.sort(key=lambda icon: icon.name)
                self.qtile.windows_map[wid] = icon

            self.conn.conn.core.ChangeSaveSet(SetMode.Insert, wid)
            self.conn.conn.core.ReparentWindow(wid, parent.wid, 0, 0)
            self.conn.conn.flush()

            info = icon.window.get_property("_XEMBED_INFO", unpack=int)

            if not info:
                self.bar.draw()
                return False

            if info[1]:
                self.bar.draw()

        return False

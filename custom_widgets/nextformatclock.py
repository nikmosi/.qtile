from zoneinfo import ZoneInfo

from libqtile import widget
from libqtile.lazy import lazy


class NextFormatsClock(widget.Clock):
    def __init__(self, formats: list, *args, **kwargs):
        self.formats = formats
        self.format_index = 0
        super().__init__(format=formats[self.format_index], *args, **kwargs)
        self.add_callback("Button1", self._left_click())
        self.add_callback("Button3", self._right_click())

    def add_callback(self, name: str, func):
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name] = self.combine(func, self.mouse_callbacks[name])
        else:
            self.mouse_callbacks[name] = func

    def combine(self, *funcs):
        @lazy.function
        def executor(qtile):
            print("execurot")
            print(len(funcs))
            for i in funcs:
                qtile.server.call((i.selectors, i.name, i.args, i.kwargs))

        return executor

    def _right_click(self):
        old_tz = self.timezone

        @lazy.function
        def wrapped(_):
            if self.timezone == old_tz:
                self.timezone = ZoneInfo("Europe/Moscow")
            else:
                self.timezone = old_tz
            self.tick()

        return wrapped()

    def _left_click(self):
        @lazy.function
        def next_clock_fomat(_):
            self.format_index += 1
            self.format_index %= len(self.formats)
            self.format = self.formats[self.format_index]
            self.update(self.poll())

        return next_clock_fomat

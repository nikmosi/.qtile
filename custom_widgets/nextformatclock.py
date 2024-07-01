from itertools import cycle
from zoneinfo import ZoneInfo

from dateutil.tz import gettz
from libqtile import widget
from libqtile.lazy import LazyCall, lazy

from utils.callbacks import combine


class NextFormatsClock(widget.Clock):
    def __init__(self, formats: list, *args, **kwargs):
        self.formats = cycle(formats)
        self.timezones = cycle([gettz(), ZoneInfo("Europe/Moscow")])
        self.timezone = next(self.timezones)
        super().__init__(format=next(self.formats), *args, **kwargs)
        self.add_callback("Button1", self._left_click())
        self.add_callback("Button3", self._right_click())

    def add_callback(self, name: str, func: LazyCall) -> None:
        if call := self.mouse_callbacks.get(name):
            self.mouse_callbacks[name] = combine(func, call)
        else:
            self.mouse_callbacks[name] = func

    def _right_click(self) -> LazyCall:
        @lazy.function
        def next_clock_timezone(_):
            self.timezone = next(self.timezones)
            self.tick()

        return next_clock_timezone

    def _left_click(self) -> LazyCall:
        @lazy.function
        def next_clock_fomat(_):
            self.format = next(self.formats)
            self.tick()

        return next_clock_fomat

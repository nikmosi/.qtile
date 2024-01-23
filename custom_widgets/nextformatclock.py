from libqtile import widget
from libqtile.lazy import lazy


class NextFormatsClock(widget.Clock):
    def __init__(self, formats: list, *args, **kwargs):
        self.formats = formats
        self.format_index = 0
        super().__init__(format=formats[self.format_index], *args, **kwargs)
        if "Button1" in self.mouse_callbacks:
            self.mouse_callbacks["Button1"] = self.combine(
                [self.click_func(), self.mouse_callbacks["Button1"]]
            )
        else:
            self.mouse_callbacks["Button1"] = self.click_func()

    def combine(self, funcs: list):
        @lazy.function
        def executor(qtile):
            print("execurot")
            print(len(funcs))
            for i in funcs:
                qtile.server.call((i.selectors, i.name, i.args, i.kwargs))

        return executor

    def click_func(self):
        @lazy.function
        def next_clock_fomat(_):
            print("format")
            self.format_index += 1
            self.format_index %= len(self.formats)
            self.format = self.formats[self.format_index]
            self.update(self.poll())

        return next_clock_fomat

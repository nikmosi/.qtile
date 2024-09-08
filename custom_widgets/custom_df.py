import subprocess as sb

from libqtile.lazy import lazy
from libqtile.widget.base import ThreadPoolText

from utils.callbacks import combine


class CDF(ThreadPoolText):
    defaults = [("format", "{}", "default format")]

    def __init__(self, text="N/A", **config):
        super().__init__(text, **config)
        key = "Button1"
        callback = lazy.function(lambda _: self.poll())
        if call := self.mouse_callbacks.get(key):
            callback = combine(callback, call)
        self.mouse_callbacks[key] = callback

    def poll(self) -> str:
        out = sb.check_output(
            "sudo btrfs filesystem usage -b /".split(), text=True
        ).split("\n")
        for i in filter(lambda a: "Used:" in a, out):
            size = float(i.split()[1]) / 1024 / 1024 / 1024
            return self.format.format(f"{size:.2f}")
        return self.text

import subprocess as sb

from libqtile.lazy import lazy
from libqtile.widget.base import ThreadPoolText
from loguru import logger

from utils.callbacks import combine


class CDF(ThreadPoolText):
    def __init__(self, text="N/A", format="{}", **config):
        self.format = format
        super().__init__(text, format=format, **config)
        key = "Button1"
        callback = lazy.function(lambda _: self.force_update())
        if call := self.mouse_callbacks.get(key):
            callback = combine(callback, call)
        self.mouse_callbacks[key] = callback

    def poll(self) -> str:  # type: ignore
        try:
            btrfs_out = sb.check_output(
                "btrfs filesystem usage -b /".split(), text=True
            ).split("\n")
        except sb.CalledProcessError as e:
            logger.warning("error from cdf sub proccess.")
            logger.warning(e)
        else:
            for i in filter(lambda a: "Used:" in a, btrfs_out):
                size = float(i.split()[1]) / 1024 / 1024 / 1024
                return self.format.format(f"{size:.2f}")
        return self.text

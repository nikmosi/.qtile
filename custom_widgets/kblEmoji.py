from libqtile import widget


class KblEmoji(widget.KeyboardLayout):
    def __init__(self, **config) -> None:
        super().__init__(**config)

    def poll(self):
        res = super().poll()
        if res == "RU":
            return "🇷🇺"
        elif res == "US":
            return "🇺🇸"
        return res

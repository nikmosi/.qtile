import subprocess as sb
from os import listdir
from os.path import isfile, join

from libqtile.lazy import lazy
from libqtile.widget.base import InLoopPollText
from loguru import logger

from custom_widgets.exceptions.wireguard import CantFindConfig
from settings import Colors as SettingColors
from utils.cli import call_rofi_dmenu


class Wireguard(InLoopPollText):
    class Color:
        green = "#55aa55"

    def __init__(
        self, configs_path="/etc/wireguard", default_text="", **config
    ) -> None:
        self.configs_path = configs_path
        text = "<span foreground='{color}' font_size='24pt'>{text}</span>"
        self.disconnected_text = text.format(
            color=SettingColors.disabled, text=default_text
        )
        self.connected_text = text.format(color=self.Color.green, text=default_text)
        self.mouse_callbacks = {"Button1": lazy.function(self.toggle_wrap())}
        logger.info(str(self.get_routable_interface()))
        super().__init__(default_text=default_text, **config)

    def get_routable_interface(self) -> list[str]:
        interfaces = sb.check_output(["networkctl"], text=True).splitlines()
        return [i.split()[1] for i in interfaces if "wireguard routable" in i]

    def select_config(self, confs: list[str]) -> str:
        if len(confs) == 1:
            return confs[0]
        assert len(confs) > 0
        config = call_rofi_dmenu(confs)
        assert config
        return config

    def toggle_wrap(self):
        def wrapper(_):
            self.toggle()

        return wrapper

    def poll(self) -> str:
        return (
            self.connected_text
            if self.get_routable_interface()
            else self.disconnected_text
        )

    def toggle(self):
        self.disconnect() if self.get_routable_interface() else self.connect()

    def disconnect(self):
        for connected_config in self.get_routable_interface():
            sb.check_call(["wg-quick", "down", connected_config])
        self.update(self.disconnected_text)

    def connect(self):
        all_files = [
            f for f in listdir(self.configs_path) if isfile(join(self.configs_path, f))
        ]
        all_configs = [i for i in all_files if i.endswith(".conf")]

        if not all_configs:
            msg = f"no configs in {self.configs_path}"
            logger.warning(msg)
            raise CantFindConfig(msg)

        selected_config = self.select_config(all_configs)

        sb.check_call(["wg-quick", "up", join(self.configs_path, selected_config)])

        self.update(self.connected_text.format(interface=selected_config))

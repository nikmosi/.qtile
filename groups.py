import re
from collections.abc import Sequence
from dataclasses import dataclass

from libqtile.config import DropDown, Group, Key, Match, ScratchPad
from libqtile.lazy import lazy

from settings import mod
from utils.converter import to_japanese_number


@dataclass
class ScreenSettings:
    index: int
    key_prefix: str
    group_count: int


def extend_keys(groups: Sequence[Group], keys_src: list[Key]) -> None:
    for i in groups:
        if not hasattr(i, "keycode"):
            continue
        key = i.keycode
        keys_src.extend(
            [
                Key(
                    [mod],
                    key,
                    lazy.group[i.name].toscreen(),
                    # lazy.group[i.name].toscreen(i.screen_affinity),
                    desc="Switch to group {}".format(i.name),
                ),
                Key(
                    [mod, "shift"],
                    key,
                    lazy.window.togroup(i.name),
                    desc="move focused window to group {}".format(i.name),
                ),
            ]
        )


def get_groups() -> Sequence[Group]:
    res = []
    for screen in [
        ScreenSettings(index=0, key_prefix="{}", group_count=6),
        ScreenSettings(index=1, key_prefix="F{}", group_count=4),
    ]:
        for i in range(1, screen.group_count + 1):
            group = Group(
                str(len(res)),
                label=str(to_japanese_number(i)),
                screen_affinity=screen.index,
            )
            res.append(group)
            setattr(group, "keycode", screen.key_prefix.format(i))

    firefox_group = Group(
        name="firefox",
        label="",
        screen_affinity=0,
        matches=[Match(wm_class="firefox")],
    )
    setattr(firefox_group, "keycode", "w")
    lazy.group[firefox_group.name].toscreen(firefox_group.screen_affinity)
    discord = Group(
        name="discord",
        label="の",
        screen_affinity=1,
        matches=[
            Match(wm_class="discord"),
            Match(wm_class="legcord"),
            Match(wm_class="vesktop"),
            Match(wm_class="ayugram-desktop"),
            Match(wm_class="anilibrix"),
            Match(wm_class="telegram-desktop"),
        ],
    )
    setattr(discord, "keycode", "semicolon")
    lazy.group[discord.name].toscreen(discord.screen_affinity)
    chatterino = Group(
        name="chatterino",
        label="󰕃",
        screen_affinity=1,
        matches=[Match(wm_class="chatterino")],
    )
    setattr(chatterino, "keycode", "b")
    lazy.group[chatterino.name].toscreen(chatterino.screen_affinity)
    minecraft = Group(
        name="minecraft",
        label="",
        screen_affinity=0,
        matches=[
            Match(title=re.compile("^Minecraft")),
            Match(wm_class="steam_proton"),
            Match(wm_class="epicgameslauncher.exe"),
            Match(wm_class="rocketleague.exe"),
            Match(wm_class="bakkesmod.exe"),
        ],
    )
    setattr(minecraft, "keycode", "m")

    res.extend([firefox_group, discord, chatterino, minecraft])
    res.append(
        ScratchPad(
            "scratchpad",
            [
                DropDown(
                    "nekoray",
                    "nekoray",
                    # match=Match(wm_class="nekoray"),
                    x=0.05,
                    y=0.2,
                    width=0.9,
                    height=0.6,
                    opacity=0.9,
                    on_focus_lost_hide=False,
                ),
            ],
        )
    )
    # lazy.group["scratchpad"].spawn("nekoray")
    return res

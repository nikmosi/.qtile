import re
from collections.abc import Sequence
from dataclasses import dataclass

from libqtile.config import Group, Key, Match
from libqtile.lazy import lazy

from settings import mod


@dataclass
class ScreenSettings:
    index: int
    key_prefix: str
    group_count: int


def extend_keys(groups: Sequence[Group], keys_src: Sequence[Key]) -> None:
    for i in groups:
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


def to_japanese_number(num: int) -> str:
    japanese_map = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
    }
    jpn_num = japanese_map.get(num)
    return jpn_num if jpn_num is not None else "Out of range"


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
            Match(wm_class="vesktop"),
            Match(wm_class="ayugram-desktop"),
            Match(wm_class="anilibrix"),
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
        matches=[Match(title=re.compile("^Minecraft"))],
    )
    setattr(minecraft, "keycode", "m")

    res.extend([firefox_group, discord, chatterino, minecraft])
    return res

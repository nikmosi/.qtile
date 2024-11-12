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

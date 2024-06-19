from settings import disabled_zero_pad


def ljust_with_disabled_zero(size: int, s: str) -> str:
    length = len(s)
    pad_size = max(0, size - length)
    return disabled_zero_pad * pad_size + s

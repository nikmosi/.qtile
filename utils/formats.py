from settings import conf


def ljust_with_disabled_zero(size: int, text: str) -> str:
    length = len(text)
    pad_size = size - length
    return conf.formats.disabled_zero_pad * pad_size + text

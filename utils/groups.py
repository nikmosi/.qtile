from collections.abc import Callable
from functools import wraps

from libqtile.config import Group


def with_screen_affinity(screen_affinity: int) -> Callable[[Group], bool]:
    @wraps(with_screen_affinity)
    def inner(group: Group) -> bool:
        return group.screen_affinity == screen_affinity

    return inner

from libqtile.config import Group


def with_screen_affinity(screen_affinity: int):
    def wrapper(group: Group) -> bool:
        return group.screen_affinity == screen_affinity

    return wrapper

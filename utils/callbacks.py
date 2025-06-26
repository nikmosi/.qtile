from libqtile.core.manager import Qtile
from libqtile.lazy import LazyCall, lazy


def combine(*funcs: LazyCall) -> LazyCall:
    @lazy.function
    def executor(qtile: Qtile):
        for i in funcs:
            qtile.server.call((i.selectors, i.name, i.args, i.kwargs, False))  # type: ignore

    return executor

from libqtile.lazy import LazyCall, lazy


def combine(self, *funcs: LazyCall):
    @lazy.function
    def executor(qtile):
        for i in funcs:
            qtile.server.call((i.selectors, i.name, i.args, i.kwargs))

    return executor

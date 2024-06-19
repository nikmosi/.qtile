from typing import Callable

from libqtile import widget
from libqtile.config import Group


class GroupBox(widget.GroupBox):
    def __init__(
        self, group_filter: Callable[[Group], bool] | None = None, *args, **kwargs
    ) -> None:
        self.group_filter = group_filter
        super().__init__(*args, **kwargs)

    @property
    def groups(self):
        su = super().groups
        if not self.group_filter:
            return su
        return [i for i in su if self.group_filter(i)]

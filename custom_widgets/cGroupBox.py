from collections.abc import Sequence
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
    def groups(self) -> Sequence[Group]:
        all_groups = super().groups
        if not self.group_filter:
            return all_groups
        return [i for i in all_groups if self.group_filter(i)]

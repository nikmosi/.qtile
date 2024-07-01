from dataclasses import dataclass

from custom_widgets.exceptions.base import CustomWidgetError


@dataclass
class ApiReject(CustomWidgetError):
    def __post_init__(self):
        self.message = "Can't get answer from api"

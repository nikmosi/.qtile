from dataclasses import dataclass

from custom_widgets.exceptions.base import CustomWidgetError


@dataclass
class CantFindConfig(CustomWidgetError): ...

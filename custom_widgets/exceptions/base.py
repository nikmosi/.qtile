from dataclasses import dataclass


@dataclass
class CustomWidgetError(Exception):
    message: str | None = None

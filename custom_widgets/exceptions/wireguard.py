from dataclasses import dataclass


@dataclass
class CantFindConfig(Exception):
    message: str

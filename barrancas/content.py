from dataclasses import dataclass
from datetime import date


@dataclass
class Page:

    title: str
    content: str
    url: str
    date: date

import re
from html.parser import HTMLParser
from typing import Any, Optional

from openatlas import app


@app.template_filter()
def sanitize(string: str, mode: Optional[str] = None) -> str:
    if not string:
        return ''
    if mode == 'text':  # Remove HTML tags, keep linebreaks
        stripper = MLStripper()
        stripper.feed(string)
        return stripper.get_data().strip()
    return re.sub('[^A-Za-z0-9]+', '', string)  # Filter ASCII letters/numbers


class MLStripper(HTMLParser):

    def error(self, message: str) -> None:
        pass  # pragma: no cover

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed: list[str] = []

    def handle_data(self, data: Any) -> None:
        self.fed.append(data)

    def get_data(self) -> str:
        return ''.join(self.fed)

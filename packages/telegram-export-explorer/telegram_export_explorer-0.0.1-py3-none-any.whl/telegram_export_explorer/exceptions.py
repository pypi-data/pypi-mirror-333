from typing import Optional

from bs4 import Tag


class MessageParsingException(Exception):
    def __init__(self, reason: str, div: Optional[Tag] = None):
        Exception.__init__(self, reason)
        self.reason = reason
        self.div = div

    def __str__(self) -> str:
        msg = self.reason
        if self.div:
            msg += "\n" + self.div.prettify()
        return msg

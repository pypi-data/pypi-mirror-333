from typing import Callable
from bs4 import Tag

from .utils import text_matches


def text_from_tag(tag: Tag) -> str:
    message_text = "".join(tag.strings).strip()
    # Remove extra whitespace
    return " ".join(message_text.split())


def html_from_tag(tag: Tag) -> str:
    html = "".join(map(str, tag.contents)).strip()
    # Remove extra whitespace
    return " ".join(html.split())


def tag_text_matches(pattern: str) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return text_matches(pattern, text_from_tag(tag))

    return f


def tag_includes_text(text: str) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return text in text_from_tag(tag)

    return f

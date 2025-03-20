from typing import Callable
from bs4 import Tag

from .exceptions import MessageParsingException
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


def tag_text_includes(text: str) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return text in text_from_tag(tag)

    return f


def tag_text_startswith(text: str) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return text_from_tag(tag).startswith(text)

    return f


def tag_text_endswith(text: str) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return text_from_tag(tag).endswith(text)

    return f


def tag_text_is(text: str) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return text_from_tag(tag) == text

    return f


def select_tag(tag: Tag, selector: str) -> Tag:
    found_tag = tag.select_one(selector)

    if found_tag is None:
        raise MessageParsingException(f'failed to select "{selector}"', tag)

    return found_tag


def select_tag_attr(tag: Tag, selector: str, attr: str) -> str:
    found_tag = select_tag(tag, selector)

    val = found_tag.attrs[attr]

    if not val:
        raise MessageParsingException(
            f'failed to select "{selector}" attr "{attr}', tag
        )

    return val


def select_tag_text(tag: Tag, selector: str) -> str:
    found_tag = select_tag(tag, selector)

    return text_from_tag(found_tag)

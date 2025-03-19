from typing import Iterable, Callable
from bs4 import Tag

from .tag_utils import tag_text_matches, text_from_tag, tag_includes_text


def tag_matches_all(
    predicates: Iterable[Callable[[Tag], bool]]
) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return all([f(tag) for f in predicates])

    return f


def tag_matches_any(
    predicates: Iterable[Callable[[Tag], bool]]
) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return any([f(tag) for f in predicates])

    return f


def is_service_message(div: Tag) -> bool:
    return "service" in div.attrs["class"]


is_invite_message = tag_matches_all(
    [is_service_message, tag_includes_text(" invited ")]
)

is_joined_group_message = tag_matches_all(
    [is_service_message, tag_includes_text(" joined group by ")]
)

is_timestamp_message = tag_matches_all(
    [is_service_message, tag_text_matches(r"\d{1,2} [A-Z][a-z]+ \d{4}")]
)


is_voice_chat_notification_message = tag_matches_all(
    [
        is_service_message,
        tag_matches_any(
            [
                tag_text_matches(r" started voice chat$"),
                tag_includes_text(" started voice chat "),
                tag_includes_text(" scheduled a voice chat "),
            ]
        ),
    ]
)

is_pinned_message = tag_matches_all(
    [
        is_service_message,
        tag_matches_all(
            [tag_includes_text(" pinned"), tag_includes_text("this message")]
        ),
    ]
)

is_group_photo_changed_message = tag_matches_all(
    [is_service_message, tag_includes_text(" changed group photo")]
)

is_group_converted_message = tag_matches_all(
    [
        is_service_message,
        tag_matches_any(
            [
                tag_includes_text(" converted this group to "),
                tag_includes_text(" converted a basic group to "),
            ]
        ),
    ]
)

is_group_name_changed_message = tag_matches_all(
    [is_service_message, tag_includes_text(" changed group title to «")]
)

messages_to_ignore = [
    is_timestamp_message,
    is_voice_chat_notification_message,
    is_pinned_message,
    is_group_photo_changed_message,
    is_group_converted_message,
]


def ignore_message(div: Tag) -> bool:
    return any(f(div) for f in messages_to_ignore)

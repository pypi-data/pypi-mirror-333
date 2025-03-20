from typing import Iterable, Callable
from bs4 import Tag

from .tag_utils import (
    tag_text_matches,
    tag_text_includes,
    tag_text_startswith,
    tag_text_endswith,
    tag_text_is,
)


def tag_matches_all(
    predicates: Iterable[Callable[[Tag], bool]],
) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return all(f(tag) for f in predicates)

    return f


def tag_matches_any(
    predicates: Iterable[Callable[[Tag], bool]],
) -> Callable[[Tag], bool]:
    def f(tag: Tag) -> bool:
        return any(f(tag) for f in predicates)

    return f


def is_service_message(div: Tag) -> bool:
    return "service" in div.attrs["class"]


is_invite_message = tag_matches_all(
    [is_service_message, tag_text_includes(" invited ")]
)

is_joined_group_message = tag_matches_all(
    [is_service_message, tag_text_includes(" joined group by ")]
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
                tag_text_includes(" started voice chat "),
                tag_text_includes(" scheduled a voice chat "),
                tag_text_is("Voice chat"),
                tag_text_startswith("Voice chat scheduled for "),
                tag_text_startswith("Voice chat ("),
            ]
        ),
    ]
)

is_pinned_message = tag_matches_all(
    [
        is_service_message,
        tag_matches_all(
            [tag_text_includes(" pinned"), tag_text_includes("this message")]
        ),
    ]
)

is_group_photo_changed_message = tag_matches_all(
    [is_service_message, tag_text_includes(" changed group photo")]
)

is_group_converted_message = tag_matches_all(
    [
        is_service_message,
        tag_matches_any(
            [
                tag_text_includes(" converted this group to "),
                tag_text_includes(" converted a basic group to "),
            ]
        ),
    ]
)

is_group_name_changed_message = tag_matches_all(
    [is_service_message, tag_text_includes(" changed group title to «")]
)

is_channel_created_message = tag_matches_all(
    [
        is_service_message,
        tag_text_startswith("Channel «"),
        tag_text_endswith("» created"),
    ]
)

is_channel_title_changed_message = tag_matches_all(
    [is_service_message, tag_text_startswith("Channel title changed to «")]
)

is_channel_photo_changed_message = tag_matches_all(
    [is_service_message, tag_text_includes("Channel photo changed")]
)

is_group_photo_removed_message = tag_matches_all(
    [is_service_message, tag_text_endswith(" removed group photo")]
)

is_user_changed_group_title_message = tag_matches_all(
    [is_service_message, tag_text_includes(" changed group title to «")]
)

is_user_removed_by_user_message = tag_matches_all(
    [is_service_message, tag_text_includes(" removed ")]
)

is_user_set_messages_to_auto_delete_message = tag_matches_all(
    [is_service_message, tag_text_endswith(" has set messages to auto-delete in")]
)

is_user_set_messages_not_to_auto_delete_message = tag_matches_all(
    [is_service_message, tag_text_endswith(" has set messages not to auto-delete")]
)

is_user_created_topic_message = tag_matches_all(
    [is_service_message, tag_text_includes(" created topic «")]
)

is_user_changed_topic_title_message = tag_matches_all(
    [is_service_message, tag_text_includes(" changed topic title to «")]
)

is_user_changed_topic_icon_message = tag_matches_all(
    [is_service_message, tag_text_includes(" changed topic icon to «")]
)

is_app_update_needed_message = tag_matches_all(
    [
        is_service_message,
        tag_text_is(
            "This message is not supported by this version of Telegram Desktop. Please update the application."  # pylint: disable=line-too-long
        ),
    ]
)

messages_to_ignore = [
    is_timestamp_message,
    is_voice_chat_notification_message,
    is_pinned_message,
    is_group_photo_changed_message,
    is_group_converted_message,
    is_channel_photo_changed_message,
    is_app_update_needed_message,
]


def ignore_message(div: Tag) -> bool:
    return any(f(div) for f in messages_to_ignore)

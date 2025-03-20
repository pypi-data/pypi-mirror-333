import mimetypes
import os
import os.path
import sqlite3
import sys


from typing import Iterator, Optional, Tuple

from bs4 import BeautifulSoup, Tag

from . import db
from . import message_matchers
from .datatypes import MediaPoll, MessageText, VideoMessageRow
from .exceptions import MessageParsingException
from .utils import parse_duration

from .tag_utils import (
    html_from_tag,
    select_tag_attr,
    select_tag_text,
    text_from_tag,
)
from .utils import parse_date_str


def make_rel_path(base: str, file: str) -> str:
    abs_base = os.path.abspath(base)
    abs_file = os.path.abspath(file)
    return abs_file.removeprefix(abs_base).removeprefix("/")


def is_messages_file(filename: str) -> bool:
    return filename.startswith("messages") and filename.endswith(".html")


def messages_files(messages_dir: str) -> Iterator[Tuple[str, str]]:
    for root, _, files in os.walk(messages_dir):
        for file in files:
            if not is_messages_file(file):
                continue

            abs_path = os.path.abspath(os.path.join(root, file))
            rel_path = make_rel_path(messages_dir, abs_path)
            yield abs_path, rel_path


def handle_invite_message(
    cur: sqlite3.Cursor, *, message_div: Tag, group_chat_id: int
) -> None:
    inviter, invitee = text_from_tag(message_div).split(" invited ")
    inviter_id = db.insert_user(cur, inviter)
    invitee_id = db.insert_user(cur, invitee)

    db.insert_group_chat_membership(
        cur, group_chat_id=group_chat_id, user_id=inviter_id
    )
    db.insert_group_chat_membership(
        cur, group_chat_id=group_chat_id, user_id=invitee_id
    )


def handle_user_removed_by_user_message(
    cur: sqlite3.Cursor, *, message_div: Tag, group_chat_id: int
) -> None:
    remover, removee = text_from_tag(message_div).split(" removed ")
    remover_id = db.insert_user(cur, remover)
    removee_id = db.insert_user(cur, removee)

    db.insert_group_chat_membership(
        cur, group_chat_id=group_chat_id, user_id=remover_id
    )
    db.insert_group_chat_membership(
        cur, group_chat_id=group_chat_id, user_id=removee_id
    )


def handle_file_attachment(
    cur: sqlite3.Cursor,
    *,
    abs_messages_file_path: str,
    rel_messages_file_path: str,
    message_id: int,
    media_file_anchor: Tag,
) -> None:
    href = media_file_anchor.attrs["href"]
    if not href:
        raise MessageParsingException(
            "unable to find file attachment href", media_file_anchor
        )

    abs_file_path = os.path.join(os.path.dirname(abs_messages_file_path), href)
    rel_file_path = os.path.join(os.path.dirname(rel_messages_file_path), href)

    title = select_tag_text(media_file_anchor, "a.media_file > div.body > div.title")

    mime_type, _ = mimetypes.guess_file_type(abs_file_path)
    if mime_type is None:
        mime_type = "unknown"

    try:
        file_size = os.stat(abs_file_path).st_size
    except FileNotFoundError:
        print(
            "unable to insert attachment, likely due to malformed unicode in filename:",
            abs_file_path,
            file=sys.stderr,
        )
        return

    db.insert_file_attachment(
        cur,
        file_path=rel_file_path,
        title=title,
        size=file_size,
        mime_type=mime_type,
        message_db_id=message_id,
    )


def handle_photo_attachment(
    cur: sqlite3.Cursor,
    *,
    abs_messages_file_path: str,
    rel_messages_file_path: str,
    message_id: int,
    photo_wrap_anchor: Tag,
) -> None:
    href = photo_wrap_anchor.attrs["href"]
    if not href:
        raise MessageParsingException(
            "unable to find photo attachment href", photo_wrap_anchor
        )

    abs_photo_path = os.path.join(os.path.dirname(abs_messages_file_path), href)
    rel_photo_path = os.path.join(os.path.dirname(rel_messages_file_path), href)

    mime_type, _ = mimetypes.guess_file_type(abs_photo_path)
    if mime_type is None:
        mime_type = "unknown"

    try:
        file_size = os.stat(abs_photo_path).st_size
    except FileNotFoundError:
        print(
            "unable to insert photo attachment, likely due to malformed unicode in filename:",
            abs_photo_path,
            file=sys.stderr,
        )
        return

    db.insert_photo_attachment(
        cur,
        file_path=rel_photo_path,
        size=file_size,
        mime_type=mime_type,
        message_db_id=message_id,
    )


def handle_video_file_wrap_anchor(
    cur: sqlite3.Cursor,
    *,
    abs_messages_file_path: str,
    rel_messages_file_path: str,
    message_id: int,
    video_file_wrap_anchor: Tag,
) -> None:
    href = video_file_wrap_anchor.attrs["href"]
    if not href:
        raise MessageParsingException(
            "unable to find video file href", video_file_wrap_anchor
        )

    abs_file_path = os.path.join(os.path.dirname(abs_messages_file_path), href)
    rel_file_path = os.path.join(os.path.dirname(rel_messages_file_path), href)

    mime_type, _ = mimetypes.guess_file_type(abs_file_path)
    if mime_type is None:
        mime_type = "unknown"

    try:
        file_size = os.stat(abs_file_path).st_size
    except FileNotFoundError:
        print(
            "unable to insert video file, likely due to malformed unicode in filename:",
            abs_file_path,
            file=sys.stderr,
        )
        return

    duration_str = select_tag_text(
        video_file_wrap_anchor, "a.video_file_wrap > div.video_duration"
    )

    duration = parse_duration(duration_str)

    thumbnail_src = select_tag_attr(
        video_file_wrap_anchor, "a.video_file_wrap > img.video_file", "src"
    )

    thumbnail_path = os.path.join(os.path.dirname(thumbnail_src), href)

    row = VideoMessageRow(
        message_id=message_id,
        path=rel_file_path,
        thumbnail_path=thumbnail_path,
        size=file_size,
        duration=duration,
        mime_type=mime_type,
    )

    db.insert_video_message(cur, row)


def handle_media_video_anchor(
    cur: sqlite3.Cursor,
    *,
    abs_messages_file_path: str,
    rel_messages_file_path: str,
    message_id: int,
    media_video_anchor: Tag,
) -> None:
    href = media_video_anchor.attrs["href"]
    if not href:
        raise MessageParsingException(
            "unable to find video file href", media_video_anchor
        )

    abs_file_path = os.path.join(os.path.dirname(abs_messages_file_path), href)
    rel_file_path = os.path.join(os.path.dirname(rel_messages_file_path), href)

    mime_type, _ = mimetypes.guess_file_type(abs_file_path)
    if mime_type is None:
        mime_type = "unknown"

    try:
        file_size = os.stat(abs_file_path).st_size
    except FileNotFoundError:
        print(
            "unable to insert video file, likely due to malformed unicode in filename:",
            abs_file_path,
            file=sys.stderr,
        )
        return

    duration_str = select_tag_text(
        media_video_anchor, "a.media_video > div.body > div.status.details"
    )

    duration = parse_duration(duration_str)

    thumbnail_src = select_tag_attr(
        media_video_anchor, "a.media_video > img.thumb", "src"
    )

    thumbnail_path = os.path.join(os.path.dirname(thumbnail_src), href)

    row = VideoMessageRow(
        message_id=message_id,
        path=rel_file_path,
        thumbnail_path=thumbnail_path,
        size=file_size,
        duration=duration,
        mime_type=mime_type,
    )

    db.insert_video_message(cur, row)


def handle_joined_group_message(
    cur: sqlite3.Cursor, *, message_div: Tag, group_chat_id: int
) -> None:
    username = text_from_tag(message_div).split(" joined group", maxsplit=1)[0].strip()
    user_id = db.insert_user(cur, username)
    db.insert_group_chat_membership(cur, group_chat_id=group_chat_id, user_id=user_id)


def store_messages_file(cur: sqlite3.Cursor, abs_path: str, rel_path: str) -> None:
    print("Parsing", abs_path)
    with open(abs_path, encoding="utf8") as f:
        html = f.read()

    html_doc = BeautifulSoup(html, "html.parser")

    chat_title = select_tag_text(html_doc, "div.page_header > .content > div.text")
    group_chat_id = db.insert_group_chat(cur, title=chat_title)

    messages_file_id = db.insert_messages_file(
        cur, filename=rel_path, group_chat_id=group_chat_id
    )

    previous_sender_id: int = -1

    for message_div in html_doc.select("div.history > div.message"):
        if not isinstance(message_div, Tag):
            raise MessageParsingException(
                "unsure how to handle" + str(type(message_div))
            )

        if message_matchers.ignore_message(message_div):
            continue

        # Handle invite messages
        if message_matchers.is_invite_message(message_div):
            handle_invite_message(
                cur, message_div=message_div, group_chat_id=group_chat_id
            )
            continue

        # Handle user removed by user message
        if message_matchers.is_user_removed_by_user_message(message_div):
            handle_user_removed_by_user_message(
                cur, message_div=message_div, group_chat_id=group_chat_id
            )
            continue

        # Handle "joined group" messages
        if message_matchers.is_joined_group_message(message_div):
            handle_joined_group_message(
                cur, message_div=message_div, group_chat_id=group_chat_id
            )
            continue

        # Handle "channel created" messages
        if message_matchers.is_channel_created_message(message_div):
            chat_name = text_from_tag(message_div).split("«")[1]
            db.insert_group_chat(cur, title=chat_name, group_chat_id=group_chat_id)
            continue

        if message_matchers.is_channel_title_changed_message(message_div):
            chat_name = text_from_tag(message_div).split("«")[1]
            db.insert_group_chat(cur, title=chat_name, group_chat_id=group_chat_id)
            continue

        # Handle group photo removed message
        if message_matchers.is_group_photo_removed_message(message_div):
            username = (
                text_from_tag(message_div)
                .split(" removed group photo", maxsplit=1)[0]
                .strip()
            )
            user_id = db.insert_user(cur, username)
            db.insert_group_chat_membership(
                cur, group_chat_id=group_chat_id, user_id=user_id
            )
            continue

        # Handle user set messages to auto-delete message
        if message_matchers.is_user_set_messages_to_auto_delete_message(message_div):
            username = (
                text_from_tag(message_div)
                .split(" created topic «", maxsplit=1)[0]
                .strip()
            )
            user_id = db.insert_user(cur, username)
            db.insert_group_chat_membership(
                cur, group_chat_id=group_chat_id, user_id=user_id
            )
            continue

        # Handle user created topic message
        if message_matchers.is_user_created_topic_message(message_div):
            username = (
                text_from_tag(message_div)
                .split(" created topic «", maxsplit=1)[0]
                .strip()
            )
            user_id = db.insert_user(cur, username)
            db.insert_group_chat_membership(
                cur, group_chat_id=group_chat_id, user_id=user_id
            )
            continue

        # Handle user changed topic title message
        if message_matchers.is_user_changed_topic_title_message(message_div):
            username = (
                text_from_tag(message_div)
                .split(" changed topic title to «", maxsplit=1)[0]
                .strip()
            )
            user_id = db.insert_user(cur, username)
            db.insert_group_chat_membership(
                cur, group_chat_id=group_chat_id, user_id=user_id
            )
            continue

        # Handle user changed topic icon message
        if message_matchers.is_user_changed_topic_icon_message(message_div):
            username = (
                text_from_tag(message_div)
                .split(" changed topic icon to «", maxsplit=1)[0]
                .strip()
            )
            user_id = db.insert_user(cur, username)
            db.insert_group_chat_membership(
                cur, group_chat_id=group_chat_id, user_id=user_id
            )
            continue

        # Handle user changed group title message
        if message_matchers.is_user_changed_group_title_message(message_div):
            div_text = text_from_tag(message_div)

            username, chat_name = div_text.split(" changed group title to «")

            user_id = db.insert_user(cur, username)
            db.insert_group_chat_membership(
                cur, group_chat_id=group_chat_id, user_id=user_id
            )

            clean_chat_name = chat_name[:-1]
            db.insert_group_chat(
                cur, title=clean_chat_name, group_chat_id=group_chat_id
            )

            continue

        # Raise an exception if we encounter an unexpected service message
        if message_matchers.is_service_message(message_div):
            raise MessageParsingException("unexpected service message", message_div)

        # Get the Telegram message id
        message_id = message_div.attrs["id"]
        if not message_id:
            raise MessageParsingException("unable to find message_id", message_div)

        # Find the timestamp of the message
        raw_timestamp = select_tag_attr(
            message_div, "div.message > div.body > div.date", "title"
        )
        iso_timestamp = parse_date_str(raw_timestamp)

        # Figure out the message sender
        message_sender_div = message_div.select_one(
            "div.message > div.body > div.from_name"
        )
        if message_sender_div:
            sender_name = text_from_tag(message_sender_div)
            sender_id = db.insert_user(cur, sender_name)
        else:
            sender_id = previous_sender_id

        previous_sender_id = sender_id

        # Parse message text, if present
        message_text: Optional[MessageText] = None
        message_text_div = message_div.select_one("div.message > div.body > div.text")
        if message_text_div:
            message_text = {
                "plain": text_from_tag(message_text_div),
                "html": html_from_tag(message_text_div),
            }

        # Parse a poll, if present
        media_poll: Optional[MediaPoll] = None
        media_poll_div = message_div.select_one(
            "div.message > div.body > div.media_wrap > div.media_poll"
        )
        if media_poll_div:
            question = select_tag_text(media_poll_div, "div > div.question")

            media_poll = {
                "question": question,
                "html": media_poll_div.prettify(),
            }

        # Save the message
        try:
            message_db_id = db.insert_message(
                cur,
                message_id=message_id,
                timestamp=iso_timestamp,
                message_text=message_text,
                group_chat_id=group_chat_id,
                messages_file_id=messages_file_id,
                sender_id=sender_id,
                media_poll=media_poll,
            )
        except Exception as e:
            print(message_div.prettify())
            raise e

        db.insert_group_chat_membership(
            cur, group_chat_id=group_chat_id, user_id=sender_id
        )

        # Parse a file attachment, if present
        media_file_anchor = message_div.select_one(
            "div.message > div.body > div.media_wrap > a.media_file"
        )
        if media_file_anchor:
            handle_file_attachment(
                cur,
                abs_messages_file_path=abs_path,
                rel_messages_file_path=rel_path,
                message_id=message_db_id,
                media_file_anchor=media_file_anchor,
            )

        # Parse a photo attachment, if present
        photo_wrap_anchor = message_div.select_one(
            "div.message > div.body > div.media_wrap > a.photo_wrap"
        )
        if photo_wrap_anchor:
            handle_photo_attachment(
                cur,
                abs_messages_file_path=abs_path,
                rel_messages_file_path=rel_path,
                message_id=message_db_id,
                photo_wrap_anchor=photo_wrap_anchor,
            )

        # Handle a video message from "video_file_wrap"
        video_file_wrap_anchor = message_div.select_one(
            "div.message > div.body > div.media_wrap > a.video_file_wrap"
        )
        if video_file_wrap_anchor:
            handle_video_file_wrap_anchor(
                cur,
                abs_messages_file_path=abs_path,
                rel_messages_file_path=rel_path,
                message_id=message_db_id,
                video_file_wrap_anchor=video_file_wrap_anchor,
            )

        # Handle a video message from "media_video"
        media_video_anchor = message_div.select_one(
            "div.message > div.body > div.media_wrap > a.media_video"
        )
        if media_video_anchor:

            if (
                select_tag_text(
                    media_video_anchor, "a.media_video > div.body > div.title"
                )
                == "Video message"
            ):
                handle_media_video_anchor(
                    cur,
                    abs_messages_file_path=abs_path,
                    rel_messages_file_path=rel_path,
                    message_id=message_db_id,
                    media_video_anchor=media_video_anchor,
                )


def build_db(input_dir: str, db_path: str) -> None:
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

    con = sqlite3.connect(db_path, autocommit=True)
    cur = con.cursor()

    try:
        db.create_tables(cur)

        for abs_path, rel_path in messages_files(input_dir):
            store_messages_file(cur, abs_path, rel_path)
    finally:
        con.close()

import os
import os.path

import sqlite3
from typing import Iterator, Optional, Tuple

from bs4 import BeautifulSoup, Tag

from . import db
from . import message_matchers
from .datatypes import MediaPoll, MessageText
from .exceptions import MessageParsingException

from .tag_utils import (
    html_from_tag,
    text_from_tag,
)
from .utils import parse_date_str


def make_rel_path(base: str, file: str) -> str:
    abs_base = os.path.abspath(base)
    abs_file = os.path.abspath(file)
    return abs_file.removeprefix(abs_base).removeprefix("/")


def is_messages_file(filename: str) -> bool:
    return filename.startswith("messages") and filename.endswith(".html")


def messages_files(dir: str) -> Iterator[Tuple[str, str]]:
    for root, dirs, files in os.walk(dir):
        for file in files:
            if not is_messages_file(file):
                continue

            abs_path = os.path.abspath(os.path.join(root, file))
            rel_path = make_rel_path(dir, abs_path)
            yield abs_path, rel_path


def find_chat_title(html_doc: Tag) -> str:
    title_div = html_doc.select_one("div.page_header > div.content > div.text")
    if not title_div:
        raise MessageParsingException("unable to find chat title", html_doc)

    return text_from_tag(title_div)


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


def handle_joined_group_message(
    cur: sqlite3.Cursor, *, message_div: Tag, group_chat_id: int
) -> None:
    username = text_from_tag(message_div).split(" joined group")[0].strip()
    user_id = db.insert_user(cur, username)
    db.insert_group_chat_membership(cur, group_chat_id=group_chat_id, user_id=user_id)


def store_messages_file(cur: sqlite3.Cursor, abs_path: str, rel_path: str) -> None:
    with open(abs_path) as f:
        html = f.read()

    html_doc = BeautifulSoup(html, "html.parser")

    chat_title = find_chat_title(html_doc)
    group_chat_id = db.insert_group_chat(cur, title=chat_title)

    messages_file_id = db.insert_messages_file(
        cur, filename=rel_path, group_chat_id=group_chat_id
    )

    previous_sender_id: int

    for message_div in html_doc.select("div.history > div.message"):
        # print(20 * "-")
        # print(message_div.prettify())

        if not isinstance(message_div, Tag):
            raise MessageParsingException(
                "unsure how to handle" + str(type(message_div))
            )

        if message_matchers.ignore_message(message_div):
            # print("^^^ Ignoring message")
            continue

        # Handle invite messages
        if message_matchers.is_invite_message(message_div):
            # print("^^^ Handling invite message")
            handle_invite_message(
                cur, message_div=message_div, group_chat_id=group_chat_id
            )
            continue

        # Handle "joined group" messages
        if message_matchers.is_joined_group_message(message_div):
            # print("^^^ Handling joined group message")
            handle_joined_group_message(
                cur, message_div=message_div, group_chat_id=group_chat_id
            )
            continue

        if message_matchers.is_group_name_changed_message(message_div):
            raise Exception("Start here")

        # Raise an exception if we encounter an unexpected service message
        if message_matchers.is_service_message(message_div):
            raise MessageParsingException("unexpected service message", message_div)

        # Get the Telegram message id
        message_id = message_div.attrs["id"]
        if not message_id:
            raise MessageParsingException("unable to find message_id", message_div)

        # Find the timestamp of the message
        message_date_div = message_div.select_one(
            "div.message > div.body > div.date[title]"
        )
        if not message_date_div:
            raise MessageParsingException("unable to find message date", message_div)

        iso_timestamp = parse_date_str(message_date_div.attrs["title"])

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
            media_poll_question_div = media_poll_div.select_one("div > div.question")
            if media_poll_question_div is None:
                raise MessageParsingException(
                    "unable to find poll question", media_poll_question_div
                )
            media_poll = {
                "question": text_from_tag(media_poll_question_div),
                "html": media_poll_div.prettify(),
            }

        db.insert_message(
            cur,
            message_id=message_id,
            timestamp=iso_timestamp,
            message_text=message_text,
            group_chat_id=group_chat_id,
            messages_file_id=messages_file_id,
            sender_id=sender_id,
            media_poll=media_poll,
        )

        db.insert_group_chat_membership(
            cur, group_chat_id=group_chat_id, user_id=sender_id
        )

        continue


def build_db(dir: str, db_path: str) -> None:
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

    con = sqlite3.connect(db_path, autocommit=True)
    cur = con.cursor()

    try:
        db.create_tables(cur)

        for abs_path, rel_path in messages_files(dir):
            store_messages_file(cur, abs_path, rel_path)
    finally:
        con.close()

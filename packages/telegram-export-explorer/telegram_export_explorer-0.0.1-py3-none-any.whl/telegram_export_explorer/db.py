from sqlite3 import Cursor
from typing import Optional


from .datatypes import MediaPoll, MessageText


def create_tables(cur: Cursor) -> None:
    cur.executescript(
        """
        CREATE TABLE group_chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );

        CREATE TABLE group_chat_aliases(
            group_chat_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            UNIQUE(group_chat_id, title) ON CONFLICT IGNORE
            FOREIGN KEY(group_chat_id) REFERENCES group_chats(id)
        );

        CREATE TABLE messages_files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_chat_id INTEGER,
            FOREIGN KEY(group_chat_id) REFERENCES group_chats(id)
        );

        CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT NOT NULL,
            group_chat_id INTEGER NOT NULL,
            messages_file_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            sender_id INTEGER NOT NULL,
            plain_text TEXT,
            html_text TEXT,
            media_poll_question TEXT,
            media_poll_html TEXT,
            UNIQUE(message_id, group_chat_id),
            FOREIGN KEY(group_chat_id) REFERENCES group_chats(id),
            FOREIGN KEY(messages_file_id) REFERENCES messages_files(id),
            FOREIGN KEY(sender_id) REFERENCES users(id)
        );

        CREATE TABLE group_chat_memberships(
            group_chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(group_chat_id) REFERENCES group_chats(id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(group_chat_id, user_id) ON CONFLICT IGNORE
        );
        """
    )


def insert_group_chat(cur: Cursor, *, title: str, id: Optional[int] = None) -> int:
    if id is None:
        cur.execute(
            "SELECT group_chat_id FROM group_chat_aliases WHERE title = ?", (title,)
        )
        row = cur.fetchone()
        if row:
            id = row[0]
        else:
            cur.execute(
                "INSERT INTO group_chats (title) VALUES (?) RETURNING id", (title,)
            )
            id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO group_chat_aliases (group_chat_id, title) VALUES (?, ?)",
        (id, title),
    )

    return id


def insert_user(cur: Cursor, name: str) -> int:
    cur.execute("SELECT id FROM users WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        id = row[0]
    else:
        cur.execute("INSERT INTO users (name) VALUES (?) RETURNING id", (name,))
        id = cur.fetchone()[0]

    return id


def insert_messages_file(cur: Cursor, *, filename: str, group_chat_id: int) -> int:
    cur.execute(
        "INSERT INTO messages_files (name, group_chat_id) VALUES (?, ?) RETURNING id",
        (filename, group_chat_id),
    )
    return cur.fetchone()[0]


def insert_message(
    cur: Cursor,
    *,
    message_id: str,
    timestamp: str,
    group_chat_id: int,
    messages_file_id: int,
    sender_id: int,
    message_text: Optional[MessageText] = None,
    media_poll: Optional[MediaPoll] = None,
) -> None:
    row = {
        "message_id": message_id,
        "group_chat_id": group_chat_id,
        "messages_file_id": messages_file_id,
        "timestamp": timestamp,
        "sender_id": sender_id,
    }

    if message_text:
        row["plain_text"] = message_text["plain"]
        row["html_text"] = message_text["html"]

    if media_poll:
        row["media_poll_question"] = media_poll["question"]
        row["media_poll_html"] = media_poll["html"]

    column_names = row.keys()
    values = row.values()
    placeholders = ", ".join(len(column_names) * "?")

    cur.execute(
        f"INSERT INTO messages ({', '.join(column_names)}) VALUES ({placeholders})",
        list(values),
    )


def insert_group_chat_membership(
    cur: Cursor, *, group_chat_id: int, user_id: int
) -> None:
    cur.execute(
        "INSERT INTO group_chat_memberships (group_chat_id, user_id) VALUES (?, ?)",
        (group_chat_id, user_id),
    )

from sqlite3 import Cursor
from typing import Optional


from .datatypes import MediaPoll, MessageText, VideoMessageRow


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

        CREATE TABLE file_attachments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT NOT NULL,
            path TEXT NOT NULL,
            title TEXT NOT NULL,
            size INTEGER NOT NULL,
            mime_type TEXT NOT NULL,
            FOREIGN KEY(message_id) REFERENCES messages(id)
        );

        CREATE TABLE photo_attachments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT NOT NULL,
            path TEXT NOT NULL,
            size INTEGER NOT NULL,
            mime_type TEXT NOT NULL,
            FOREIGN KEY(message_id) REFERENCES messages(id)
        );

        CREATE TABLE video_messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT NOT NULL,
            path TEXT NOT NULL,
            thumbnail_path TEXT NOT NULL,
            size INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            mime_type TEXT NOT NULL,
            FOREIGN KEY(message_id) REFERENCES messages(id)
        );
        """
    )


def insert_group_chat(
    cur: Cursor, *, title: str, group_chat_id: Optional[int] = None
) -> int:
    if group_chat_id is None:
        cur.execute(
            "SELECT group_chat_id FROM group_chat_aliases WHERE title = ?", (title,)
        )
        row = cur.fetchone()
        if row:
            group_chat_id = row[0]
        else:
            cur.execute(
                "INSERT INTO group_chats (title) VALUES (?) RETURNING id", (title,)
            )
            group_chat_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO group_chat_aliases (group_chat_id, title) VALUES (?, ?)",
        (group_chat_id, title),
    )

    return group_chat_id


def insert_user(cur: Cursor, name: str) -> int:
    cur.execute("SELECT id FROM users WHERE name = ?", (name,))
    row = cur.fetchone()

    user_id: int

    if row:
        user_id = row[0]
    else:
        cur.execute("INSERT INTO users (name) VALUES (?) RETURNING id", (name,))
        user_id = cur.fetchone()[0]

    return user_id


def insert_messages_file(cur: Cursor, *, filename: str, group_chat_id: int) -> int:
    cur.execute(
        "INSERT INTO messages_files (name, group_chat_id) VALUES (?, ?) RETURNING id",
        (filename, group_chat_id),
    )

    messages_file_id: int = cur.fetchone()[0]
    return messages_file_id


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
) -> int:
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
        f"INSERT INTO messages ({', '.join(column_names)}) VALUES ({placeholders}) RETURNING id",
        list(values),
    )

    message_db_id: int = cur.fetchone()[0]
    return message_db_id


def insert_group_chat_membership(
    cur: Cursor, *, group_chat_id: int, user_id: int
) -> None:
    cur.execute(
        "INSERT INTO group_chat_memberships (group_chat_id, user_id) VALUES (?, ?)",
        (group_chat_id, user_id),
    )


def insert_file_attachment(
    cur: Cursor,
    *,
    file_path: str,
    title: str,
    size: int,
    mime_type: str,
    message_db_id: int,
) -> None:
    cur.execute(
        "INSERT INTO file_attachments (message_id, path, title, size, mime_type) VALUES (?, ?, ?, ?, ?)",  # pylint: disable=line-too-long
        (message_db_id, file_path, title, size, mime_type),
    )


def insert_photo_attachment(
    cur: Cursor,
    *,
    file_path: str,
    size: int,
    mime_type: str,
    message_db_id: int,
) -> None:
    cur.execute(
        "INSERT INTO photo_attachments (message_id, path, size, mime_type) VALUES (?, ?, ?, ?)",  # pylint: disable=line-too-long
        (message_db_id, file_path, size, mime_type),
    )


def insert_video_message(cur: Cursor, row: VideoMessageRow) -> None:
    cur.execute(
        """
        INSERT INTO video_messages (
            message_id,
            path,
            thumbnail_path,
            size,
            duration,
            mime_type
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row.message_id,
            row.path,
            row.thumbnail_path,
            row.size,
            row.duration,
            row.mime_type,
        ),
    )

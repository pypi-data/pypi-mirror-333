from dataclasses import dataclass
from typing import Optional, TypedDict


class MessageText(TypedDict):
    plain: str
    html: str


class MediaPoll(TypedDict):
    question: str
    html: str


@dataclass
class VideoMessageRow:
    message_id: int
    path: str
    thumbnail_path: str
    size: int
    duration: int
    mime_type: str
    id: Optional[int] = None

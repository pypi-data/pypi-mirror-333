from typing import Optional, TypedDict


class MessageText(TypedDict):
    plain: str
    html: str


class MediaPoll(TypedDict):
    question: str
    html: str

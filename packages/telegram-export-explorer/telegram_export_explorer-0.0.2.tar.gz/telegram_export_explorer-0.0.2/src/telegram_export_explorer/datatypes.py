from typing import TypedDict


class MessageText(TypedDict):
    plain: str
    html: str


class MediaPoll(TypedDict):
    question: str
    html: str

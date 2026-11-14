from dataclasses import dataclass
from typing import Protocol


@dataclass
class Question:
    id: int | None
    text: str
    answer: str


class AssistantUnavailable(Exception):
    pass


class Assistant(Protocol):
    def answer(self, text: str) -> str: ...


class QuestionRepository(Protocol):
    def list_recent(self, limit: int) -> list[Question]: ...

    def add(self, text: str, answer: str) -> Question: ...

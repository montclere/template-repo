import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.domain.question import AssistantUnavailable

TEST_DB = Path(__file__).parent / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
TEST_DB.unlink(missing_ok=True)


class FakeAssistant:
    """Replaces the ml service in tests. Set `down = True` to simulate an outage."""

    def __init__(self):
        self.down = False

    def answer(self, text: str) -> str:
        if self.down:
            raise AssistantUnavailable("ml is down")
        return f"ответ на: {text}"


@pytest.fixture
def assistant():
    return FakeAssistant()


@pytest.fixture
def client(assistant):
    # Imported here so that DATABASE_URL above is set before the engine is created.
    from app.api.deps import get_assistant
    from app.main import app

    app.dependency_overrides[get_assistant] = lambda: assistant
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

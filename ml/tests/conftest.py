import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class FakeLLM(BaseHTTPRequestHandler):
    """Stands in for the model API. Tests set `reply_text` and queue `statuses`."""

    reply_text = "hello"
    statuses: list[int] = []
    requests: list[dict] = []
    log_path: Path

    def log_message(self, *args):
        pass

    def do_POST(self):
        length = int(self.headers["content-length"])
        FakeLLM.requests.append(
            {
                "path": self.path,
                "key": self.headers["x-api-key"],
                "body": json.loads(self.rfile.read(length)),
            }
        )
        status = FakeLLM.statuses.pop(0) if FakeLLM.statuses else 200
        reply = {
            "content": [{"type": "text", "text": FakeLLM.reply_text}],
            "usage": {"input_tokens": 3, "output_tokens": 1},
        }
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(reply).encode())


@pytest.fixture
def fake_llm(tmp_path, monkeypatch):
    server = HTTPServer(("127.0.0.1", 0), FakeLLM)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    FakeLLM.reply_text = "hello"
    FakeLLM.statuses = []
    FakeLLM.requests = []
    FakeLLM.log_path = tmp_path / "llm.log.jsonl"
    monkeypatch.setattr(settings, "llm_base_url", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setattr(settings, "llm_model", "test-model")
    monkeypatch.setattr(settings, "anthropic_api_key", "test-key")
    monkeypatch.setattr(settings, "llm_log_path", str(FakeLLM.log_path))
    monkeypatch.setattr(settings, "llm_retry_delay_seconds", 0)
    yield FakeLLM
    server.shutdown()
    server.server_close()

import json
import urllib.error
import urllib.request

from app.domain.question import AssistantUnavailable


class MlClient:
    """HTTP client for the ml service. Implements the `Assistant` protocol."""

    def __init__(self, base_url: str, timeout_seconds: float):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def answer(self, text: str) -> str:
        request = urllib.request.Request(
            f"{self.base_url}/api/v1/ask",
            data=json.dumps({"question": text}).encode(),
            method="POST",
            headers={"content-type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read())["answer"]
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise AssistantUnavailable(f"ml returned {error.code}: {detail}") from error
        except (urllib.error.URLError, TimeoutError) as error:
            reason = getattr(error, "reason", error)
            raise AssistantUnavailable(
                f"ml is not reachable at {self.base_url}: {reason}"
            ) from error
        except (ValueError, KeyError, TypeError) as error:
            raise AssistantUnavailable(f"ml returned an unexpected response: {error}") from error

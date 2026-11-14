import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from app.config import settings
from app.llm.client import LLMError, complete
from app.llm.prompts import load_prompt

HERE = Path(__file__).parent
CASES = HERE / "cases.jsonl"
RESULTS = HERE / "results"
BASE_URL = os.environ.get("ML_URL", "http://localhost:8100")
REQUEST_TIMEOUT_SECONDS = 120


def call(method: str, path: str, body):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        BASE_URL + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as error:
        return error.code, None


def dig(value, dotted: str):
    for key in dotted.split("."):
        if isinstance(value, list):
            value = value[int(key)]
        elif isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    return value


def check_code(case: dict, status: int, payload) -> str:
    check = case["check"]
    if "status" in check and status != check["status"]:
        return "FAIL"
    actual = dig(payload, check["field"]) if "field" in check else payload
    if "equals" in check and actual != check["equals"]:
        return "FAIL"
    if "contains" in check and check["contains"] not in str(actual):
        return "FAIL"
    return "PASS" if status < 400 or "status" in check else "FAIL"


def check_tool(case: dict, status: int, payload) -> str:
    check = case["check"]
    calls = dig(payload, check.get("field", "tool_calls")) or []
    names = [c.get("name") if isinstance(c, dict) else c for c in calls]
    return "PASS" if status < 400 and check["called"] in names else "FAIL"


def check_judge(case: dict, status: int, payload) -> str:
    if not settings.llm_model or not settings.anthropic_api_key:
        return "SKIP"
    prompt = load_prompt("judge").format(
        rubric=case["rubric"],
        request=json.dumps(case.get("body"), ensure_ascii=False),
        response=json.dumps(payload, ensure_ascii=False),
    )
    try:
        reply = complete(prompt)
        verdict = json.loads(reply[reply.index("{") : reply.rindex("}") + 1])
        passed = verdict["pass"] is True
    except (LLMError, ValueError, KeyError) as error:
        print(f"      judge could not grade {case['id']}: {error}")
        return "FAIL"
    if not passed:
        print(f"      judge on {case['id']}: {verdict.get('reason')}")
    return "PASS" if passed else "FAIL"


CHECKS = {"code": check_code, "tool": check_tool, "judge": check_judge}


def run_case(case: dict) -> str:
    status, payload = call(case.get("method", "POST"), case["path"], case.get("body"))
    return CHECKS[case["type"]](case, status, payload)


def commit_hash() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "nogit"


def previous_results() -> dict:
    files = sorted(RESULTS.glob("*.json"), key=lambda f: f.stat().st_mtime)
    return json.loads(files[-1].read_text()) if files else {}


def main() -> int:
    lines = CASES.read_text(encoding="utf-8").splitlines()
    cases = [json.loads(line) for line in lines if line.strip()]
    before = previous_results()
    try:
        results = {case["id"]: run_case(case) for case in cases}
    except urllib.error.URLError as error:
        print(f"ml service is not reachable at {BASE_URL}: {error.reason}")
        print("start it with `make ml-dev` or `make up`")
        return 2

    for case_id, result in results.items():
        regression = result == "FAIL" and before.get(case_id) == "PASS"
        print(f"{result:4}  {case_id}{'  <- regression' if regression else ''}")

    counted = [r for r in results.values() if r != "SKIP"]
    passed = counted.count("PASS")
    print(f"\n{passed}/{len(counted)} passed, {len(results) - len(counted)} skipped")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{commit_hash()}.json").write_text(json.dumps(results, indent=2))
    return 0 if passed == len(counted) else 1


if __name__ == "__main__":
    sys.exit(main())

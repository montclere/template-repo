from pathlib import Path

from app.config import settings


def load_prompt(name: str) -> str:
    return (Path(settings.prompts_dir) / f"{name}.md").read_text(encoding="utf-8")

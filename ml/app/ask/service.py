from app.llm.client import complete
from app.llm.prompts import load_prompt


def answer(question: str) -> str:
    return complete(question, system=load_prompt("ask"))

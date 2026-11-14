from fastapi import APIRouter, HTTPException

from app.api.schemas.ask import AskRequest, AskResponse
from app.ask.service import answer
from app.llm.client import LLMError

router = APIRouter(tags=["ask"])


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    try:
        return AskResponse(answer=answer(payload.question))
    except LLMError as error:
        raise HTTPException(status_code=502, detail=f"model call failed: {error}") from error

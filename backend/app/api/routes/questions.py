from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_question_service
from app.api.schemas.question import QuestionCreate, QuestionRead
from app.domain.question import AssistantUnavailable
from app.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=list[QuestionRead])
def list_questions(service: QuestionService = Depends(get_question_service)):
    return [QuestionRead.model_validate(q) for q in service.history()]


@router.post("", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def ask_question(payload: QuestionCreate, service: QuestionService = Depends(get_question_service)):
    try:
        question = service.ask(payload.text)
    except AssistantUnavailable as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error
    return QuestionRead.model_validate(question)

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.domain.question import Assistant
from app.infra.db.question_repository import SqlQuestionRepository
from app.infra.db.session import get_db
from app.infra.ml_client import MlClient
from app.services.question_service import QuestionService


@lru_cache
def get_assistant() -> Assistant:
    return MlClient(base_url=settings.ml_url, timeout_seconds=settings.ml_timeout_seconds)


def get_question_service(
    db: Session = Depends(get_db), assistant: Assistant = Depends(get_assistant)
) -> QuestionService:
    return QuestionService(SqlQuestionRepository(db), assistant)

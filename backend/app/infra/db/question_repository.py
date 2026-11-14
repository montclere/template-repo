from sqlalchemy.orm import Session

from app.domain.question import Question
from app.infra.db.models import QuestionModel


class SqlQuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_recent(self, limit: int) -> list[Question]:
        rows = self.db.query(QuestionModel).order_by(QuestionModel.id.desc()).limit(limit).all()
        return [_to_entity(row) for row in rows]

    def add(self, text: str, answer: str) -> Question:
        row = QuestionModel(text=text, answer=answer)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return _to_entity(row)


def _to_entity(row: QuestionModel) -> Question:
    return Question(id=row.id, text=row.text, answer=row.answer)

from sqlalchemy import Column, Integer, Text

from app.infra.db.session import Base


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

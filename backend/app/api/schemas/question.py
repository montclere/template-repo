from pydantic import BaseModel, ConfigDict, Field


class QuestionCreate(BaseModel):
    text: str = Field(min_length=1)


class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    answer: str

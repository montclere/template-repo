from app.domain.question import Assistant, Question, QuestionRepository

HISTORY_LIMIT = 20


class QuestionService:
    def __init__(self, repository: QuestionRepository, assistant: Assistant):
        self.repository = repository
        self.assistant = assistant

    def ask(self, text: str) -> Question:
        answer = self.assistant.answer(text)
        return self.repository.add(text, answer)

    def history(self) -> list[Question]:
        return self.repository.list_recent(HISTORY_LIMIT)

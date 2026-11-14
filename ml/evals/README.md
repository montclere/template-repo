# Эвалы

Запуск: `make eval` из корня при запущенном сервисе `ml` (`make ml-dev` или `make up`) и с ключом модели в `ml/.env`.
Правила — в `docs/playbooks/evals.md`.

Случай — одна строка JSON в `cases.jsonl`:

```
{"id": "ask-returns", "type": "code", "path": "/api/v1/ask", "body": {"question": "Срок возврата?"}, "check": {"field": "answer", "contains": "14 дней"}}
{"id": "creates-task", "type": "tool", "path": "/api/v1/agent", "body": {"message": "Создай задачу на завтра"}, "check": {"field": "tool_calls", "called": "create_task"}}
{"id": "tone", "type": "judge", "path": "/api/v1/ask", "body": {"question": "..."}, "rubric": "Ответ вежливый и без выдуманных фактов"}
```

- `code`: `check.field` — путь к полю ответа через точку; `equals` или `contains`; необязательный `status`.
- `tool`: в поле `check.field` ответа лежит список вызовов инструментов; проверяется, что среди них есть `called`.
- `judge`: модель оценивает ответ по `rubric` (промпт в `prompts/judge.md`). Без `LLM_MODEL` и `ANTHROPIC_API_KEY` в `ml/.env` случай помечается `SKIP`.

Три случая в шаблоне проверяют пример `/api/v1/ask`: по одному на `code` со статусом, `code` с подстрокой и `judge`. Замените их своими, когда замените пример.

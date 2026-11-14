---
name: task-breakdown
description: Split a large piece of work into small, ordered tasks that each work end to end and can be checked. Use when a brief or spec section is too big for one task, when the task list in docs/BRIEF.md or docs/TASKS.md has to be written or re-cut, or right before starting a task to write its steps.
---

# Task breakdown

Tasks go into `docs/BRIEF.md` («Задачи») or `docs/TASKS.md` for a long project. No separate plan files.

## Cutting tasks

- A task is a vertical slice: something a person can see or call works after it, from screen to answer. Not "backend for X", then "frontend for X".
- T1 is the skeleton: the demo scenario runs end to end on stubs.
- Each task maps to a judging criterion (`K<n>`) or a requirement (`REQ<n>`). A task that maps to none goes to «Не делаем».
- Each task has a «Готово, когда» that can be checked by a command or a click, not by opinion.
- Setup, config and docs fold into the task that needs them; they are not tasks of their own.
- If you can't say what to build without finding something out first, make a research task `R<n>`: no code, the result is a conclusion in `docs/PROGRESS.md`.
- Order by risk: the part most likely not to work (model quality, an external API, data) goes first.

## Steps inside a task

Right before starting, write the steps under the task, grouped by part:

```
- [ ] **T2. Ответ со ссылкой на источник.** Критерий: K1. Готово, когда: в ответе есть ссылка, eval `cites-source` проходит
  - [ ] контракт: поле `sources` в `AskResponse` (ml) и `QuestionRead` (backend)
  - [ ] ml: промпт `prompts/ask.md`, разбор ответа модели, eval-случай
  - [ ] backend: сохранить и вернуть `sources`
  - [ ] frontend: ссылки под ответом
  - [ ] проверка: `make check`, `make smoke`, `make eval`
```

- Name exact files, endpoints and fields; no "add error handling" or "write tests" without saying which.
- Skip parts the task doesn't touch.
- The check line always lists the commands from the hard rules in `AGENTS.md`.

## Self-check

- Every criterion or requirement is covered by some task, or is in «Не делаем» on purpose.
- Names of fields and endpoints match between tasks.
- No task depends on one that comes after it.

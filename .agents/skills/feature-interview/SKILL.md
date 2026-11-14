---
name: feature-interview
description: Turn the materials in docs/input/ into docs/BRIEF.md (or docs/SPEC.md for a long project), asking the user at most five questions about gaps. Use at project start when asked to fill the brief or spec, or when the user brings a new idea that is not in the brief yet. Not for ordinary tasks already listed in the brief.
---

# Feature interview

## 1. Read everything first

Read every file in `docs/input/`, then the template you will fill: `docs/BRIEF.md`, or `docs/SPEC.md` if the project uses `docs/long-project/`. Never edit `docs/input/`.

## 2. Find the gaps

List for yourself what the template needs and the inputs don't answer, or answer in two contradicting ways. Typical gaps:

- Who the user is and the one moment of the demo that must impress.
- Judging criteria and their weights; deadline and submission format.
- What the AI part takes in and gives out; where its data comes from.
- Whether a plain model call is enough, or retrieval or an agent is really needed (`docs/playbooks/agents.md`, `rag.md`).
- The three risk questions from `docs/playbooks/security.md`.
- What is real and what is a stub in the demo; what happens if the model API is down.

Don't ask about anything the files already answer or that you can decide yourself at low cost.

## 3. Ask — at most five questions in total

- One round if possible, two at most. Ask the most important gaps; decide the rest yourself and mark those decisions in the brief as «решено агентом» so the user can overrule them.
- Every question has 2–3 concrete options labelled A/B/C. Mark the one you recommend and say in one line why (speed, judging criteria, risk). The user may answer with just a letter.
- Use AskUserQuestion when it is available; otherwise a numbered list in chat.

## 4. Write the result

- Fill every section of the template. Status stays «черновик» — only the user approves.
- Tasks: 5–8, each one working end to end and mapped to at least one criterion; T1 is the skeleton on stubs. Use the `task-breakdown` skill if the task list is hard to cut.
- Anything outside the demo scenario or the criteria goes to «Не делаем».
- Finish with a short summary in chat: what you decided yourself, and what the user should check first.

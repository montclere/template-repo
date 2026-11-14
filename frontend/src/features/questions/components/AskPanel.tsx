import { type FormEvent, useState } from "react";

import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";

import { useQuestions } from "../hooks/useQuestions";

export function AskPanel() {
  const { questions, pending, error, ask } = useQuestions();
  const [text, setText] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!text.trim()) return;
    if (await ask(text.trim())) setText("");
  }

  return (
    <section className="space-y-4">
      <form onSubmit={submit} className="flex gap-2">
        <Input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Задайте вопрос"
          disabled={pending}
        />
        <Button type="submit" disabled={pending || !text.trim()}>
          {pending ? "Думаю…" : "Спросить"}
        </Button>
      </form>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <ul className="space-y-3">
        {questions.map((q) => (
          <li key={q.id} className="rounded-md border border-border p-3">
            <p className="text-sm font-medium">{q.text}</p>
            <p className="mt-1 text-sm text-muted-foreground whitespace-pre-wrap">{q.answer}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}

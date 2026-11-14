import { apiFetch } from "@/shared/api/client";

import type { Question } from "./types";

export function listQuestions() {
  return apiFetch<Question[]>("/api/v1/questions");
}

export function askQuestion(text: string) {
  return apiFetch<Question>("/api/v1/questions", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

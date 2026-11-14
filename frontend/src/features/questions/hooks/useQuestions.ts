import { useCallback, useEffect, useState } from "react";

import { askQuestion, listQuestions } from "../api";
import type { Question } from "../types";

export function useQuestions() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listQuestions()
      .then(setQuestions)
      .catch((e: Error) => setError(e.message));
  }, []);

  const ask = useCallback(async (text: string) => {
    setPending(true);
    setError(null);
    try {
      const created = await askQuestion(text);
      setQuestions((current) => [created, ...current]);
      return true;
    } catch (e) {
      setError((e as Error).message);
      return false;
    } finally {
      setPending(false);
    }
  }, []);

  return { questions, pending, error, ask };
}

import { AskPanel } from "@/features/questions/components/AskPanel";

export function App() {
  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-4 text-xl font-semibold">Вопрос к ИИ</h1>
      <AskPanel />
    </main>
  );
}

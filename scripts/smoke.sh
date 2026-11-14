#!/usr/bin/env bash
# Сквозная проверка запущенного стека (make up или три *-dev команды).
# Допишите сюда шаги своего сценария демо из docs/BRIEF.md.
set -u

BACKEND="${BACKEND_URL:-http://localhost:8000}"
ML="${ML_URL:-http://localhost:8100}"
FRONTEND="${FRONTEND_URL:-http://localhost:5173}"
failed=0

step() {
  local name="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "ok    $name"; else echo "FAIL  $name"; failed=1; fi
}

body_has() {
  local expected="$1"; shift
  curl -fsS --max-time 60 "$@" | grep -q "$expected"
}

[ -d backend ]  && step "backend health"  body_has '"ok"' "$BACKEND/api/v1/health"
[ -d ml ]       && step "ml health"       body_has '"ok"' "$ML/api/v1/health"
[ -d frontend ] && step "frontend opens"  curl -fsS --max-time 20 -o /dev/null "$FRONTEND"
[ -d backend ] && [ -d ml ] && \
  step "вопрос: backend -> ml -> модель" body_has '"answer"' -X POST "$BACKEND/api/v1/questions" \
    -H 'Content-Type: application/json' -d '{"text":"Скажи одно слово: работает"}'

if [ $failed -ne 0 ]; then
  echo
  echo "Если упал только шаг с вопросом: проверьте LLM_MODEL и ANTHROPIC_API_KEY в ml/.env"
  echo "и последнюю строку ml/logs/llm.log.jsonl."
fi

exit $failed

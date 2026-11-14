# frontend

Vite + React + TS. Organized by feature, not by file type. Talks only to the backend.

## Rules

- `features/<name>/{api.ts,types.ts,components/,hooks/}` — a feature owns everything it needs. Create a subfolder when it has a file to hold. The example is `features/questions`.
- `shared/` — only code used by 2+ features (api client, ui primitives, helpers).
- A feature may import from `shared/`, never from another feature's internals.
- `app/` — shell only: routing, layout, providers. No business logic.
- Imports: `@/...` (points at `src/`) across folders, relative paths inside one feature.
- API base URL comes from `VITE_API_URL`. Never hardcode the backend host.
- UI primitives come from shadcn/ui, styled with Tailwind. Add one with `npx shadcn@latest add <name>` — it lands in `shared/ui/`. Don't hand-roll a primitive shadcn already has.
- Merge conditional classNames with `cn()` from `shared/lib/utils.ts`.
- Show loading and error states for every request: the demo will hit a slow or failing model.

## Commands

- `npm install && npm run dev`
- `npm run format && npm run lint`
- `npx tsc -b` — type check (CI runs it)

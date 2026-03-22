# Trackaboo — Claude Code Conventions

## Project Overview
Trackaboo is a personal financial tracking app built with:
- **Framework**: Next.js 15 (App Router), TypeScript strict mode
- **Database**: SQLite via Drizzle ORM + better-sqlite3
- **UI**: shadcn/ui + Tailwind CSS + Recharts (charts)
- **Validation**: Zod (shared between client and server)
- **State/Data**: SWR for client-side data fetching
- **Forms**: react-hook-form + Zod resolver

---

## Architecture First Principles

| Principle | Rule |
|-----------|------|
| **API-first** | Update `openapi.yaml` before implementing any route |
| **Schema-first** | Update `src/db/schema.ts` before any DB access code; run `npm run db:generate` |
| **No assumptions** | Every non-obvious decision has a `// Decision:` comment inline |
| **Extensible** | New transaction types (investment, transfer) add new tables, not modify existing ones |
| **No direct DB** | Components and hooks never import from `src/db/` — only via `/api/v1/` routes |
| **No `any`** | TypeScript strict mode; use `unknown` + narrowing |

---

## Skills Workflow

Use the appropriate skill for each type of work:

| Task | Skill to invoke |
|------|----------------|
| Design a new feature or extend schema | `senior-architect` |
| Implement a feature, route, or component | `senior-nextjs-engineer` |
| Review code before marking complete | `senior-code-reviewer` |
| Publish release notes at a milestone | `senior-release-engineer` |

**Mandatory rule**: Always invoke `senior-code-reviewer` after `senior-nextjs-engineer` completes a feature.

---

## Directory Conventions

```
src/
├── app/
│   ├── (dashboard)/dashboard/   # All user-facing pages
│   └── api/v1/                  # All API routes — no DB access elsewhere
├── components/
│   ├── ui/                      # shadcn/ui — never hand-edit; use `npx shadcn@latest add`
│   ├── layout/                  # AppShell, Sidebar, TopBar
│   ├── dashboard/               # Dashboard-specific components
│   ├── inflow/                  # Inflow-specific components
│   ├── outflow/                 # Outflow-specific components
│   └── shared/                  # Reusable across features
├── db/
│   ├── schema.ts                # Single source of truth for data shapes
│   └── index.ts                 # DB singleton — import this, not better-sqlite3 directly
├── hooks/                       # SWR hooks — one file per resource
├── lib/
│   ├── api/                     # Typed fetch client
│   ├── validations/             # Zod schemas — shared client + server
│   └── formatters.ts            # Currency, date, percentage formatters
└── types/                       # TypeScript types derived from Zod/Drizzle
```

---

## Coding Standards

### TypeScript
- Strict mode is on — no `any`, no `@ts-ignore`
- Use `unknown` and narrow with Zod `.safeParse()` or type guards
- All Drizzle results typed via `$inferSelect` / `$inferInsert`

### API Routes
- All inputs validated with Zod **before** any DB operation
- Error responses: `{ error: string, issues?: ZodIssue[] }`
- 5xx responses: `{ error: "Internal server error" }` — no stack traces in production

### Database
- ORM: Drizzle ORM with better-sqlite3 (synchronous)
- Migrations: `npm run db:generate` → `npm run db:migrate` (never edit migration files manually)
- Amounts: stored as `real` (float64); formatted for display via `src/lib/formatters.ts`
- Dates: always `YYYY-MM-DD` text strings (no timezone, no datetime)
- FK constraints: always define `onDelete` behaviour

### Components
- Presentational components: no direct API calls, no DB imports
- Data flows: page → SWR hook → `/api/v1/` route → DB
- Forms: always use react-hook-form + Zod resolver with the shared validation schema

---

## Environment Variables

Required variables (see `.env.example`):
```
DATABASE_URL=./trackaboo.db    # Path to SQLite file (relative to project root)
NODE_ENV=development
```

- Never commit `.env.local` — the pre-push hook enforces this
- Add new variables to `.env.example` with a comment explaining each one

---

## Testing

- Unit tests: co-located as `*.test.ts` next to the file under test
- Integration tests: `src/__tests__/`
- Runner: `npm test` (Vitest)
- **Minimum per API route**: happy path + validation failure + edge case
- Tests must not rely on a real DB file — use in-memory SQLite

---

## Common Commands

```bash
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build
npm run db:generate  # Generate SQL migration from schema changes
npm run db:migrate   # Apply pending migrations
npm run db:studio    # Open Drizzle Studio (visual DB browser)
npm test             # Run all tests
npm run lint         # Type-check (tsc --noEmit)
```

---

## Git Conventions

- **Branches**: `feat/`, `fix/`, `chore/`, `docs/`
- **Commits**: Conventional Commits — `feat:`, `fix:`, `chore:`, `docs:`
- **Never commit**: `.env.local`, `*.db`, `node_modules/`, `.next/`
- Pre-push hook scans for secrets automatically

---

## Adding a New Feature — Step by Step

1. Invoke `senior-architect` → get schema + API design (updates `openapi.yaml` + `src/db/schema.ts`)
2. Run `npm run db:generate` + `npm run db:migrate`
3. Invoke `senior-nextjs-engineer` → implement routes, hooks, components, tests
4. Invoke `senior-code-reviewer` → verify before closing the feature
5. On milestone completion → invoke `senior-release-engineer` → update `CHANGELOG.md`

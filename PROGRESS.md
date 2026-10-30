# Build progress (read this first when resuming)

Resume rule: when the owner writes "continue", pick up at the first unchecked item below.

## Environment limits seen while building (Stage 1)
The build sandbox had no network: packages could not be installed, so FastAPI/React tests and builds were NOT
run there. Run them in CI (GitHub Actions) or locally; see "Verified" below for what actually ran.

## Stage 1 — foundation
- [x] Monorepo layout, .gitignore, .env.example
- [x] Backend: config, JSON logging, security middleware (headers, rate limit, origin check), crypto helper
- [x] Models for all 25 required entities (UUID ids, FKs, indexes, constraints, timestamps)
- [x] Alembic baseline migration
- [x] Firebase ID-token verification, single-owner initialisation (OWNER_EMAIL), ownership helper, audit events
- [x] SSRF guard, storage interface (local + S3), honest integration status
- [x] Agent runtime (timeout, retries, cancel, progress, logs, tool/secret allow-lists) + registry of 16 agents
- [x] API: health, /api/me, projects CRUD, research targets, dashboard, agents, integrations
- [x] Frontend: PWA shell, dark/light themes, sidebar + mobile bottom nav, login, Overview, Projects,
      AI Research (target intake), AI Agents, Security Center, Settings; honest "not built" pages for the rest
- [x] Docker, compose, CI workflow, Railway notes, tests written
- [x] Docs: ARCHITECTURE, LOCAL_DEVELOPMENT, GITHUB_SETUP, RAILWAY_DEPLOYMENT, FIREBASE_AUTH_SETUP,
      ENVIRONMENT_VARIABLES, DATABASE_SETUP, BACKUP_AND_RECOVERY, SECURITY, API_DOCUMENTATION, USER_GUIDE
- [ ] Push to GitHub and get first green CI run (owner action)

## Stage 2 — research + browser automation (not started)
Playwright worker, SSRF-safe browsing, screenshots, research report generation, prompt-injection handling,
worker heartbeat, WebSocket progress, Browser Lab controls, notifications bell.
## Stage 3 — recording, desktop companion, device pairing (not started)
## Stage 4 — scripts, voice, FFmpeg, editor, subtitles, thumbnails (not started)
## Stage 5 — YouTube OAuth, upload, scheduling, approvals (not started)
## Stage 6 — analytics, security center extras, notifications, monitoring, backups (not started)

## Verified in the build sandbox
- SSRF guard: executed against 9 hostile URLs, all blocked; public IP allowed.
- Agent runtime: executed retry, timeout, permission denial, cancellation, bad input.
- All backend Python compiles; docker-compose and CI YAML parse.
- Frontend: no TypeScript syntax errors. Full typecheck/tests/build NOT run (no packages).

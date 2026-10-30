# HELL UPLOADS

Private, single-owner AI platform for researching websites and apps, recording real demos, producing tutorial
videos and publishing to YouTube.

**Status: Stage 1 of 6.** Foundation only. See [PROGRESS.md](PROGRESS.md) for exactly what works and what is
not built. Nothing is simulated: unbuilt sections say so.

## Quick start (local)
```bash
cp .env.example .env            # set OWNER_EMAIL and Firebase values
docker compose up -d postgres redis
cd backend && python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
pytest -q                        # run the backend tests
uvicorn app.main:app --reload    # http://localhost:8000/docs
# second terminal
cd frontend && cp .env.example .env && npm install && npm test && npm run dev   # http://localhost:5173
```
Full guides are in [docs/](docs/).

# Trackaboo

Personal financial tracking app — track inflows, outflows, and monthly category breakdowns.

**Stack**: Vue 3 + TypeScript (frontend) · Python FastAPI (backend) · SQLite

---

## Project Structure

```
trackaboo/
├── backend/          # Python FastAPI — REST API + SQLite via SQLAlchemy
├── frontend/         # Vue 3 + Vite — SPA served from the same container
├── openapi.yaml      # API contract (source of truth)
├── Dockerfile        # Single-container build (POC)
└── trackaboo.db      # SQLite database (local dev only — not committed)
```

---

## Running Locally

### Prerequisites
- Node.js 20+ (or use [nvm](https://github.com/nvm-sh/nvm))
- Python 3.12+

### Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env             # Default: DATABASE_URL=../trackaboo.db

# Start the API server (hot-reload)
uvicorn app.main:app --reload --port 8000
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy and configure environment
cp .env.example .env.local       # Default: VITE_API_BASE_URL=http://localhost:8000/api/v1

# Start the dev server
npm run dev
```

App available at `http://localhost:5173`

### Tests

```bash
# Backend (pytest)
cd backend
source .venv/bin/activate
pytest tests/ -v

# Frontend (vitest)
cd frontend
npm test
```

---

## Docker (Single Container — POC)

Builds the Vue frontend, then serves both the static app and the API from a single FastAPI process on port 8000.

### Build and run

```bash
# Build the image
docker build -t trackaboo .

# Run with a persistent data volume
docker run -d \
  --name trackaboo \
  -p 8000:8000 \
  -v trackaboo-data:/data \
  trackaboo
```

App + API available at `http://localhost:8000`

### Rebuild after code changes

```bash
docker stop trackaboo && docker rm trackaboo
docker build -t trackaboo .
docker run -d --name trackaboo -p 8000:8000 -v trackaboo-data:/data trackaboo
```

### Using Docker Compose (optional)

```yaml
# docker-compose.yml
services:
  trackaboo:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - trackaboo-data:/data

volumes:
  trackaboo-data:
```

```bash
docker compose up --build
```

---

## API Reference

Full contract in [`openapi.yaml`](./openapi.yaml). Key endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/metrics?month=YYYY-MM` | Monthly totals + category breakdown |
| GET/POST | `/api/v1/inflows` | List / create inflows |
| GET/PATCH/DELETE | `/api/v1/inflows/{id}` | Single inflow |
| GET/POST | `/api/v1/outflows` | List / create outflows |
| GET/PATCH/DELETE | `/api/v1/outflows/{id}` | Single outflow |
| GET/POST | `/api/v1/categories` | List / create categories |
| GET/PATCH/DELETE | `/api/v1/categories/{id}` | Single category |

---

## Development Notes

- Amounts stored as `REAL` (float64); displayed via `formatCurrency()` in frontend
- Dates stored as `YYYY-MM-DD` text (no timezone)
- `outflows.category_id` is NOT NULL — every outflow must have a category
- `inflows.category_id` is nullable
- Delete a category that has outflows → 409 Conflict
- Backend tests use in-memory SQLite (never touch `trackaboo.db`)

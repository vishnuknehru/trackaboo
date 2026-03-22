# ─── Stage 1: Build Vue 3 frontend ───────────────────────────────────────────
FROM node:24-alpine AS frontend-builder

WORKDIR /build/frontend

COPY frontend/package*.json ./
RUN npm ci --silent

COPY frontend/ .
RUN npm run build
# Output: /build/frontend/dist/


# ─── Stage 2: Python FastAPI — serves both API and built frontend ─────────────
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/app/ ./app/

# Copy built Vue frontend from stage 1
COPY --from=frontend-builder /build/frontend/dist/ ./frontend/dist/

# Database lives in a volume so data persists across container restarts.
# Point DATABASE_URL at the volume mount path.
ENV DATABASE_URL=/data/trackaboo.db
ENV FRONTEND_DIST=/app/frontend/dist

VOLUME ["/data"]

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

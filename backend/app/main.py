from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.database import create_all_tables
from app.routers import health, metrics, categories, inflows, outflows


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create tables on startup (idempotent — does nothing if they exist)."""
    create_all_tables()
    yield


app = FastAPI(
    title="Trackaboo API",
    version="0.1.0",
    description="Personal financial tracking backend",
    lifespan=lifespan,
)

# Decision: CORS allows localhost dev servers; in Docker the frontend is served
# by this same process so CORS is not needed, but kept for local dev convenience.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_PREFIX = "/api/v1"

app.include_router(health.router, prefix=_PREFIX, tags=["health"])
app.include_router(metrics.router, prefix=_PREFIX, tags=["metrics"])
app.include_router(categories.router, prefix=_PREFIX, tags=["categories"])
app.include_router(inflows.router, prefix=_PREFIX, tags=["inflows"])
app.include_router(outflows.router, prefix=_PREFIX, tags=["outflows"])

# Decision: when FRONTEND_DIST is set (Docker / production), serve the built
# Vue app from the same process. API routes registered above take priority over
# the catch-all SPA fallback below because FastAPI resolves routes in order.
_FRONTEND_DIST = os.getenv("FRONTEND_DIST")
if _FRONTEND_DIST:
    _dist = Path(_FRONTEND_DIST)
    _assets = _dist / "assets"
    if _assets.exists():
        app.mount("/assets", StaticFiles(directory=str(_assets)), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str) -> FileResponse:
        """SPA fallback — Vue Router handles client-side routing."""
        return FileResponse(str(_dist / "index.html"))


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all: never expose stack traces in production.
    Decision: re-raise HTTPException so FastAPI's built-in handler processes it
    with the correct status code; only swallow truly unexpected exceptions.
    """
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

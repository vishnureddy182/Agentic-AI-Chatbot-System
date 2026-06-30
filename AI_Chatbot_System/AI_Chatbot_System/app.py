"""
app.py — [MVP] Application entry point.

Boots the FastAPI app, wires up middleware, mounts routers, and exposes
/health for the Week 1 "Done when..." check:
    docker compose up  ->  /health returns 200

Run locally:
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")


# ---------------------------------------------------------------------------
# Lifespan — startup/shutdown hooks (DB connections, model warm-up, etc.)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s in '%s' mode...", settings.APP_NAME, settings.APP_ENV)

    # --- Startup ---
    # database/db_operations.py: open a pooled connection / run a ping.
    try:
        from database.db_operations import init_db

        await init_db()
        logger.info("Database connection initialized.")
    except ModuleNotFoundError:
        # Week 1 scaffold may run before database/db_operations.py exists yet.
        logger.warning("database.db_operations not found — skipping DB init (expected pre-Week-1 build).")
    except Exception as exc:
        logger.error("Database initialization failed: %s", exc)

    yield

    # --- Shutdown ---
    logger.info("Shutting down %s...", settings.APP_NAME)


# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise RAG + Multi-Agent eCommerce Chatbot Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# security/cors_policy.py owns the production-grade CORS rules (Week 5+).
try:
    from security.cors_policy import apply_cors_policy

    apply_cors_policy(app)
except ModuleNotFoundError:
    logger.warning("security.cors_policy not found yet — using permissive default CORS (Week 1 scaffold).")

# observability/logging_middleware.py: structured request/response logging.
try:
    from observability.logging_middleware import LoggingMiddleware

    app.add_middleware(LoggingMiddleware)
except ModuleNotFoundError:
    logger.warning("observability.logging_middleware not found yet — skipping (build in Week 6+).")


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": str(exc) if settings.DEBUG else "Something went wrong."},
    )


# ---------------------------------------------------------------------------
# Routers — mounted as they're built (Week 5+)
# ---------------------------------------------------------------------------
_ROUTER_MODULES = [
    ("routers.chat", "router", "/chat", "chat"),
    ("routers.auth", "router", "/auth", "auth"),
    ("routers.documents", "router", "/documents", "documents"),
    ("routers.feedback", "router", "/feedback", "feedback"),
    ("routers.admin", "router", "/admin", "admin"),
]

for module_path, attr_name, prefix, tag in _ROUTER_MODULES:
    try:
        module = __import__(module_path, fromlist=[attr_name])
        router = getattr(module, attr_name)
        app.include_router(router, prefix=f"{settings.API_V1_PREFIX}{prefix}", tags=[tag])
        logger.info("Mounted router: %s -> %s%s", module_path, settings.API_V1_PREFIX, prefix)
    except ModuleNotFoundError:
        logger.warning("%s not found yet — skipping (build per Week 5-6 plan).", module_path)


# ---------------------------------------------------------------------------
# Health check — the Week 1 "Done when..." target
# ---------------------------------------------------------------------------
@app.get("/health", tags=["system"])
async def health():
    """Liveness/readiness probe. docker compose up -> this must return 200."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }


@app.get("/", tags=["system"])
async def root():
    return {
        "message": f"{settings.APP_NAME} is running.",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

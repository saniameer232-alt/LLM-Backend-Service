from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.models import router as models_router
from app.core.logging import setup_logging


# -----------------------------------
# Logging
# -----------------------------------

setup_logging()


# -----------------------------------
# FastAPI Application
# -----------------------------------

app = FastAPI(
    title="LLM Backend Service",
    version="1.0.0",
    description="Production-ready LLM backend service",
)


# -----------------------------------
# Routes
# -----------------------------------

app.include_router(health_router)
app.include_router(models_router)
app.include_router(chat_router)
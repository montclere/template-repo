from fastapi import FastAPI

from app.api.routes import ask, health

app = FastAPI(title="ml")

app.include_router(health.router, prefix="/api/v1")
app.include_router(ask.router, prefix="/api/v1")

from fastapi import FastAPI
from app.core.config import settings
from app.presentation.api.health import router as health_router
from app.presentation.api.teams import router as teams_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(teams_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} API ishlamoqda",
        "docs_url": "/docs",
    }
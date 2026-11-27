from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.middleware import ObservabilityMiddleware
from app.presentation.api.auth import router as auth_router
from app.presentation.api.health import router as health_router
from app.presentation.api.matches import router as matches_router
from app.presentation.api.monitoring import router as monitoring_router
from app.presentation.api.notifications import router as notifications_router
from app.presentation.api.players import router as players_router
from app.presentation.api.teams import router as teams_router
from app.presentation.api.tournaments import router as tournaments_router

setup_logging()

STATIC_DIR = Path(__file__).resolve().parent / "presentation" / "static"

tags_metadata = [
    {"name": "Tizim holati", "description": "Server ishlayotganini va joriy versiyani tekshirish."},
    {"name": "Autentifikatsiya", "description": "Ro'yxatdan o'tish, JWT token olish va profilni tekshirish."},
    {"name": "Jamoalar", "description": "Havaskor futbol jamoalarini boshqarish."},
    {"name": "O'yinchilar", "description": "Jamoalarga futbolchilarni biriktirish."},
    {"name": "Turnirlar", "description": "Musobaqalar va turnir jadvalini olish."},
    {"name": "Uchrashuvlar", "description": "O'yinlarni rejalashtirish va hisob kiritish."},
    {"name": "Hodisalar va bildirishnomalar", "description": "EventBus orqali hosil bo'lgan jonli bildirishnomalar."},
    {"name": "Monitoring va metrikalar", "description": "Jurnallar, Prometheus metrikalari va baza holati."},
]

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    description=(
        "Havaskor futbol turnirlarini tashkil etish, jamoalar va o'yinchilarni ro'yxatdan o'tkazish, "
        "uchrashuv natijalarini kiritish hamda turnir jadvalini avtomatik hisoblash uchun REST API."
    ),
    openapi_tags=tags_metadata,
    contact={
        "name": "Toirov Azizjon",
        "url": "https://github.com/azizjontoirov/football-system",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ObservabilityMiddleware)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(teams_router, prefix=settings.API_V1_PREFIX)
app.include_router(players_router, prefix=settings.API_V1_PREFIX)
app.include_router(tournaments_router, prefix=settings.API_V1_PREFIX)
app.include_router(matches_router, prefix=settings.API_V1_PREFIX)
app.include_router(notifications_router, prefix=settings.API_V1_PREFIX)
app.include_router(monitoring_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Tizim holati"], summary="Asosiy kirish nuqtasi")
def root():
    return {
        "message": f"{settings.APP_NAME} API ishlamoqda",
        "ui_url": "/ui",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get("/ui", include_in_schema=False)
def web_dashboard():
    return FileResponse(STATIC_DIR / "index.html")
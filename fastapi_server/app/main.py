from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database.crud import init_db
from app.api import auth, cars, diagnostics, keys, firmware, reports

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запуск та зупинка сервера"""
    logger.info("🚀 Запуск AutoSpark API...")
    await init_db()
    logger.info("✅ База даних ініціалізована")
    yield
    logger.info("👋 Сервер зупинено")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API для автосервісу AutoSpark — діагностика, ключі, прошивки",
    lifespan=lifespan,
)

# CORS для Flutter додатку
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У продакшені — конкретні домени
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(auth.router)
app.include_router(cars.router)
app.include_router(diagnostics.router)
app.include_router(keys.router)
app.include_router(firmware.router)
app.include_router(reports.router)


@app.get("/")
async def root():
    return {
        "app_d": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
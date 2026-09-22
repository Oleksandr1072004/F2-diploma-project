from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.crud import get_db, get_cars, get_car_by_vin, create_car
from app.database.schemas import CarCreate, CarResponse
from app.database.models import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/cars", tags=["Cars"])


@router.get("/", response_model=List[CarResponse])
async def list_cars(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Список всіх автомобілів"""
    return await get_cars(db, skip, limit)


@router.get("/vin/{vin}", response_model=CarResponse)
async def get_car_by_vin_endpoint(
    vin: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Пошук авто по VIN"""
    car = await get_car_by_vin(db, vin)
    if not car:
        raise HTTPException(status_code=404, detail="Авто не знайдено")
    return car


@router.post("/", response_model=CarResponse, status_code=201)
async def add_car(
    car: CarCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Додати нове авто"""
    return await create_car(db, car)
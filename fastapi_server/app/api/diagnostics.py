from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.crud import (
    get_db, get_diagnostics, get_diagnostics_by_car, create_diagnostic
)
from app.database.schemas import DiagnosticCreate, DiagnosticResponse
from app.database.models import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/diagnostics", tags=["Diagnostics"])


@router.get("/", response_model=List[DiagnosticResponse])
async def list_diagnostics(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Всі діагностики"""
    return await get_diagnostics(db, skip, limit)


@router.get("/car/{car_id}", response_model=List[DiagnosticResponse])
async def get_car_diagnostics(
    car_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Історія діагностики авто"""
    return await get_diagnostics_by_car(db, car_id)


@router.post("/", response_model=DiagnosticResponse, status_code=201)
async def add_diagnostic(
    diagnostic: DiagnosticCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Додати нову діагностику"""
    return await create_diagnostic(db, diagnostic, current_user.id)
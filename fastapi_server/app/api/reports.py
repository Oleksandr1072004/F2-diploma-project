from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from app.database.crud import get_db, get_car_by_vin, get_diagnostics_by_car
from app.database.models import User
from app.api.auth import get_current_user
from app.services.pdf_generator import generate_diagnostic_report

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/diagnostic/{car_id}")
async def download_diagnostic_report(
        car_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Завантажити PDF звіт діагностики"""
    diagnostics = await get_diagnostics_by_car(db, car_id)
    if not diagnostics:
        raise HTTPException(status_code=404, detail="Діагностик не знайдено")

    # Генеруємо PDF
    pdf_path = await generate_diagnostic_report(car_id, diagnostics)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"diagnostic_{car_id}.pdf",
    )
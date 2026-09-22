from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import get_db, create_firmware_log
from app.database.schemas import FirmwareLogCreate, FirmwareLogResponse
from app.database.models import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/firmware", tags=["Firmware"])


@router.post("/", response_model=FirmwareLogResponse, status_code=201)
async def log_firmware(
    firmware: FirmwareLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Записати лог прошивки"""
    return await create_firmware_log(db, firmware, current_user.id)
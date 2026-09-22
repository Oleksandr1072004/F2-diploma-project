from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import get_db, create_key_registration
from app.database.schemas import KeyRegistrationCreate, KeyRegistrationResponse
from app.database.models import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/keys", tags=["Key Registration"])


@router.post("/", response_model=KeyRegistrationResponse, status_code=201)
async def register_key(
    key: KeyRegistrationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Зареєструвати новий ключ"""
    return await create_key_registration(db, key, current_user.id)
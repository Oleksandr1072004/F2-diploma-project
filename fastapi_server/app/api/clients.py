from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.crud import get_db, get_clients, get_client, create_client
from app.database.schemas import ClientCreate, ClientResponse
from app.database.models import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get("/", response_model=List[ClientResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Список всіх клієнтів"""
    return await get_clients(db, skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_by_id(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отримати клієнта за ID"""
    client = await get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клієнта не знайдено")
    return client


@router.post("/", response_model=ClientResponse, status_code=201)
async def add_client(
    client: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Створити нового клієнта"""
    return await create_client(db, client)
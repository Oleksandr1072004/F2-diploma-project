from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from typing import Optional, List

from app.database.models import Base, User, Client, Car, Diagnostic, KeyRegistration, FirmwareLog, Booking
from app.database.schemas import (
    UserCreate, ClientCreate, CarCreate, DiagnosticCreate,
    KeyRegistrationCreate, FirmwareLogCreate, BookingCreate
)
from app.config import settings


# Створення async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Створення всіх таблиць"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency для FastAPI"""
    async with AsyncSessionLocal() as session:
        yield session


# === Users CRUD ===
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate, hashed_password: str) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# === Clients CRUD ===
async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Client]:
    result = await db.execute(select(Client).offset(skip).limit(limit))
    return result.scalars().all()


async def get_client(db: AsyncSession, client_id: int) -> Optional[Client]:
    result = await db.execute(select(Client).where(Client.id == client_id))
    return result.scalar_one_or_none()


async def create_client(db: AsyncSession, client: ClientCreate) -> Client:
    db_client = Client(**client.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client


# === Cars CRUD ===
async def get_cars(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Car]:
    result = await db.execute(select(Car).offset(skip).limit(limit))
    return result.scalars().all()


async def get_car_by_vin(db: AsyncSession, vin: str) -> Optional[Car]:
    result = await db.execute(select(Car).where(Car.vin == vin))
    return result.scalar_one_or_none()


async def create_car(db: AsyncSession, car: CarCreate) -> Car:
    db_car = Car(**car.model_dump())
    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)
    return db_car


# === Diagnostics CRUD ===
async def get_diagnostics(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Diagnostic]:
    result = await db.execute(select(Diagnostic).offset(skip).limit(limit))
    return result.scalars().all()


async def get_diagnostics_by_car(db: AsyncSession, car_id: int) -> List[Diagnostic]:
    result = await db.execute(
        select(Diagnostic).where(Diagnostic.car_id == car_id).order_by(Diagnostic.created_at.desc())
    )
    return result.scalars().all()


async def create_diagnostic(db: AsyncSession, diagnostic: DiagnosticCreate, master_id: int) -> Diagnostic:
    db_diag = Diagnostic(
        **diagnostic.model_dump(),
        master_id=master_id,
    )
    db.add(db_diag)
    await db.commit()
    await db.refresh(db_diag)
    return db_diag


# === Keys CRUD ===
async def create_key_registration(
    db: AsyncSession, key: KeyRegistrationCreate, master_id: int
) -> KeyRegistration:
    db_key = KeyRegistration(**key.model_dump(), master_id=master_id)
    db.add(db_key)
    await db.commit()
    await db.refresh(db_key)
    return db_key


# === Firmware CRUD ===
async def create_firmware_log(
    db: AsyncSession, firmware: FirmwareLogCreate, master_id: int
) -> FirmwareLog:
    db_fw = FirmwareLog(**firmware.model_dump(), master_id=master_id)
    db.add(db_fw)
    await db.commit()
    await db.refresh(db_fw)
    return db_fw


# === Bookings CRUD ===
async def get_bookings(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Booking]:
    result = await db.execute(select(Booking).offset(skip).limit(limit))
    return result.scalars().all()


async def create_booking(db: AsyncSession, booking: BookingCreate) -> Booking:
    db_booking = Booking(**booking.model_dump())
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking
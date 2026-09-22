from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List


# === Users ===
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "master"


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# === Clients ===
class ClientBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    telegram_id: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# === Cars ===
class CarBase(BaseModel):
    vin: Optional[str] = Field(None, max_length=17)
    brand: str
    model: str
    year: Optional[int] = None
    engine_type: Optional[str] = None
    transmission: Optional[str] = None
    license_plate: Optional[str] = None
    mileage: Optional[int] = None
    notes: Optional[str] = None


class CarCreate(CarBase):
    client_id: int


class CarResponse(CarBase):
    id: int
    client_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# === Diagnostics ===
class DiagnosticBase(BaseModel):
    car_id: int
    ecu_type: Optional[str] = None
    dtc_codes: List[str] = []
    live_data: Optional[dict] = None
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None


class DiagnosticCreate(DiagnosticBase):
    pass


class DiagnosticResponse(DiagnosticBase):
    id: int
    master_id: Optional[int] = None
    report_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# === Keys ===
class KeyRegistrationBase(BaseModel):
    car_id: int
    key_type: str
    chip_type: Optional[str] = None
    serial_number: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None


class KeyRegistrationCreate(KeyRegistrationBase):
    pass


class KeyRegistrationResponse(KeyRegistrationBase):
    id: int
    master_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# === Firmware ===
class FirmwareLogBase(BaseModel):
    car_id: int
    ecu_type: str
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    checksum_before: Optional[str] = None
    checksum_after: Optional[str] = None
    success: bool = False
    notes: Optional[str] = None


class FirmwareLogCreate(FirmwareLogBase):
    pass


class FirmwareLogResponse(FirmwareLogBase):
    id: int
    master_id: Optional[int] = None
    backup_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# === Bookings ===
class BookingBase(BaseModel):
    client_id: int
    car_id: Optional[int] = None
    service_type: str
    scheduled_at: datetime
    status: str = "pending"
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean,
    ForeignKey, Text, JSON, Numeric
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """Користувачі системи (майстри, адміни)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="master")  # admin, master
    is_active = Column(Boolean, default=True)
    telegram_id = Column(String(20), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Зв'язки
    diagnostics = relationship("Diagnostic", back_populates="master")
    firmware_logs = relationship("FirmwareLog", back_populates="master")


class Client(Base):
    """Клієнти автосервісу"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(20), unique=True, nullable=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Зв'язки
    cars = relationship("Car", back_populates="client", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="client")


class Car(Base):
    """Автомобілі клієнтів"""
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))
    vin = Column(String(17), unique=True, index=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer)
    engine_type = Column(String(30))
    transmission = Column(String(30))
    license_plate = Column(String(20))
    mileage = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Зв'язки
    client = relationship("Client", back_populates="cars")
    diagnostics = relationship("Diagnostic", back_populates="car")
    firmware_logs = relationship("FirmwareLog", back_populates="car")
    key_registrations = relationship("KeyRegistration", back_populates="car")
    bookings = relationship("Booking", back_populates="car")


class Diagnostic(Base):
    """Діагностика автомобіля"""
    __tablename__ = "diagnostics"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
    master_id = Column(Integer, ForeignKey("users.id"))
    ecu_type = Column(String(20))  # ECU, TCU, SRS, BODY, ODO, ABS
    dtc_codes = Column(JSON, default=list)  # список кодів помилок
    live_data = Column(JSON)  # показники датчиків
    symptoms = Column(Text)  # опис симптомів
    diagnosis = Column(Text)  # висновок
    recommendations = Column(Text)  # рекомендації
    report_path = Column(String(255))  # PDF звіт
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Зв'язки
    car = relationship("Car", back_populates="diagnostics")
    master = relationship("User", back_populates="diagnostics")


class KeyRegistration(Base):
    """Реєстрація ключів"""
    __tablename__ = "key_registrations"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
    master_id = Column(Integer, ForeignKey("users.id"))
    key_type = Column(String(30))  # Transponder, Smart Key, Remote
    chip_type = Column(String(30))  # ID48, ID46, 4D, 8A
    serial_number = Column(String(50))
    status = Column(String(20), default="pending")  # pending, success, failed
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="key_registrations")


class FirmwareLog(Base):
    """Логування прошивок"""
    __tablename__ = "firmware_logs"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
    master_id = Column(Integer, ForeignKey("users.id"))
    ecu_type = Column(String(20))  # ECU, TCU, SRS, BODY, ODO
    old_version = Column(String(50))
    new_version = Column(String(50))
    checksum_before = Column(String(64))
    checksum_after = Column(String(64))
    backup_path = Column(String(255))
    success = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="firmware_logs")
    master = relationship("User", back_populates="firmware_logs")


class Booking(Base):
    """Записи на сервіс"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="SET NULL"), nullable=True)
    service_type = Column(String(50))  # diagnostics, keys, optics, etc.
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="bookings")
    car = relationship("Car", back_populates="bookings")
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

    patient = relationship(
        "Patient",
        back_populates="user",
        uselist=False,
    )

    doctor = relationship(
        "Doctor",
        back_populates="user",
        uselist=False,
    )


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    date_of_birth = Column(String)
    phone = Column(String)
    address = Column(String)
    previous_health_history = Column(Text)

    user = relationship(
        "User",
        back_populates="patient",
    )

    appointments = relationship(
        "Appointment",
        back_populates="patient",
    )


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    specialty = Column(String)
    available_days = Column(String)
    available_times = Column(String)

    user = relationship(
        "User",
        back_populates="doctor",
    )

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
    )
    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
    )
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String, default="booked", nullable=False)
    reason_for_visit = Column(Text)
    notes = Column(Text)

    patient = relationship(
        "Patient",
        back_populates="appointments",
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments",
    )

    notifications = relationship(
        "Notification",
        back_populates="appointment",
    )


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        nullable=False,
    )
    message = Column(Text)
    sent_status = Column(
        String,
        default="pending",
        nullable=False,
    )

    appointment = relationship(
        "Appointment",
        back_populates="notifications",
    )

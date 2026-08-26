from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(..., min_length=3, max_length=30)

    phone: str | None = Field(default=None, max_length=30)
    address: str | None = Field(default=None, max_length=255)
    previous_health_history: str | None = None

    specialty: str | None = Field(default=None, max_length=100)
    available_days: str | None = Field(default=None, max_length=100)
    available_times: str | None = Field(default=None, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    appointment_datetime: datetime
    reason_for_visit: str = Field(..., min_length=1, max_length=1000)


class AppointmentUpdate(BaseModel):
    appointment_datetime: datetime | None = None
    status: str | None = Field(default=None, max_length=30)
    notes: str | None = Field(default=None, max_length=2000)


class ChatMessage(BaseModel):
    role: str = Field(..., min_length=1, max_length=30)
    content: str = Field(..., min_length=1, max_length=10000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    user_id: int | None = Field(default=None, gt=0)
    role: str | None = Field(default=None, max_length=30)


class IntentRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

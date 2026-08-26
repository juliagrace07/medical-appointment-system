from datetime import date, datetime, time

from sqlalchemy.orm import Session

import models


def calculate_age(date_of_birth: str | None) -> int | None:
    """Calculate a patient's age from an ISO-formatted date string."""

    if not date_of_birth:
        return None

    try:
        year, month, day = map(int, date_of_birth.split("-"))
        dob = date(year, month, day)
        today = date.today()

        return (
            today.year
            - dob.year
            - ((today.month, today.day) < (dob.month, dob.day))
        )

    except (ValueError, TypeError):
        return None


def get_doctor_by_user_id(
    db: Session,
    user_id: int,
):
    """Return the doctor profile associated with a user account."""

    return (
        db.query(models.Doctor)
        .filter(models.Doctor.user_id == user_id)
        .first()
    )


def get_patient_by_user_id(
    db: Session,
    user_id: int,
):
    """Return the patient profile associated with a user account."""

    return (
        db.query(models.Patient)
        .filter(models.Patient.user_id == user_id)
        .first()
    )


def get_all_doctors(db: Session):
    """Return all doctor profiles."""

    return (
        db.query(models.Doctor)
        .order_by(models.Doctor.id)
        .all()
    )


def get_doctor_by_name(
    db: Session,
    doctor_name: str,
):
    """Find a doctor using a case-insensitive partial name match."""

    if not doctor_name.strip():
        return None

    search_name = doctor_name.strip().lower()

    doctors = db.query(models.Doctor).all()

    for doctor in doctors:
        if not doctor.user or not doctor.user.name:
            continue

        current_name = doctor.user.name.lower()

        if (
            search_name in current_name
            or current_name in search_name
        ):
            return doctor

    return None


def get_doctor_schedule_summary(
    db: Session,
    doctor_id: int,
):
    """Return a doctor's specialty and general availability."""

    doctor = (
        db.query(models.Doctor)
        .filter(models.Doctor.id == doctor_id)
        .first()
    )

    if not doctor:
        return None

    return {
        "doctor_name": doctor.user.name,
        "specialty": doctor.specialty,
        "available_days": doctor.available_days,
        "available_times": doctor.available_times,
    }


def get_doctor_upcoming_appointments(
    db: Session,
    doctor_id: int,
):
    """Return upcoming booked appointments for a doctor."""

    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor_id,
            models.Appointment.appointment_datetime >= datetime.now(),
            models.Appointment.status == "booked",
        )
        .order_by(models.Appointment.appointment_datetime)
        .all()
    )


def get_doctor_all_appointments(
    db: Session,
    doctor_id: int,
):
    """Return all appointments associated with a doctor."""

    return (
        db.query(models.Appointment)
        .filter(models.Appointment.doctor_id == doctor_id)
        .order_by(models.Appointment.appointment_datetime)
        .all()
    )


def get_doctor_appointments_today(
    db: Session,
    doctor_id: int,
):
    """Return today's booked appointments for a doctor."""

    today = date.today()

    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)

    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor_id,
            models.Appointment.appointment_datetime >= start,
            models.Appointment.appointment_datetime <= end,
            models.Appointment.status == "booked",
        )
        .order_by(models.Appointment.appointment_datetime)
        .all()
    )


def get_doctor_next_appointment(
    db: Session,
    doctor_id: int,
):
    """Return the next booked appointment for a doctor."""

    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor_id,
            models.Appointment.appointment_datetime >= datetime.now(),
            models.Appointment.status == "booked",
        )
        .order_by(models.Appointment.appointment_datetime)
        .first()
    )


def get_doctor_all_patients(
    db: Session,
    doctor_id: int,
):
    """Return unique patients who have appointments with a doctor."""

    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.doctor_id == doctor_id)
        .all()
    )

    patients_by_id = {}

    for appointment in appointments:
        if appointment.patient:
            patients_by_id[appointment.patient.id] = appointment.patient

    return list(patients_by_id.values())


def get_patient_appointments(
    db: Session,
    patient_id: int,
):
    """Return appointments associated with a patient."""

    return (
        db.query(models.Appointment)
        .filter(models.Appointment.patient_id == patient_id)
        .order_by(models.Appointment.appointment_datetime)
        .all()
    )


def search_patients_by_condition(
    db: Session,
    condition: str,
):
    """Find patients whose recorded health history contains a term."""

    if not condition or not condition.strip():
        return []

    return (
        db.query(models.Patient)
        .filter(
            models.Patient.previous_health_history.ilike(
                f"%{condition.strip()}%"
            )
        )
        .all()
    )


def search_patients_by_city(
    db: Session,
    city: str,
):
    """Find patients whose address contains a city or location."""

    if not city or not city.strip():
        return []

    return (
        db.query(models.Patient)
        .filter(
            models.Patient.address.ilike(
                f"%{city.strip()}%"
            )
        )
        .all()
    )


def search_patients_under_age(
    db: Session,
    age_limit: int,
):
    """Return patients whose calculated age is below the provided limit."""

    if age_limit <= 0:
        return []

    patients = db.query(models.Patient).all()

    result = []

    for patient in patients:
        age = calculate_age(patient.date_of_birth)

        if age is not None and age < age_limit:
            result.append(patient)

    return result


def search_patients_generic(
    db: Session,
    condition: str | None = None,
    city: str | None = None,
    age_lt: int | None = None,
    age_gt: int | None = None,
    name: str | None = None,
):
    """
    Search patients using optional condition, location,
    age, and name filters.
    """

    patients = db.query(models.Patient).all()
    results = []

    condition = condition.strip().lower() if condition else None
    city = city.strip().lower() if city else None
    name = name.strip().lower() if name else None

    for patient in patients:
        patient_name = (
            patient.user.name.lower()
            if patient.user and patient.user.name
            else ""
        )

        address = (
            patient.address.lower()
            if patient.address
            else ""
        )

        history = (
            patient.previous_health_history.lower()
            if patient.previous_health_history
            else ""
        )

        age = calculate_age(patient.date_of_birth)

        if condition and condition not in history:
            continue

        if city and city not in address:
            continue

        if name and name not in patient_name:
            continue

        if age_lt is not None:
            if age is None or age >= age_lt:
                continue

        if age_gt is not None:
            if age is None or age <= age_gt:
                continue

        results.append(
            {
                "name": patient.user.name,
                "phone": patient.phone,
                "address": patient.address,
                "date_of_birth": patient.date_of_birth,
                "age": age,
                "history": patient.previous_health_history,
            }
        )

    return results

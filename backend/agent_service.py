import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()


MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"
REQUEST_TIMEOUT_SECONDS = 20


ALLOWED_INTENTS = {
    "doctor_schedule_today",
    "doctor_all_appointments",
    "doctor_upcoming_appointments",
    "doctor_all_patients",
    "doctor_next_patient",
    "doctor_next_patient_history",
    "patient_my_appointments",
    "patient_available_doctors",
    "patient_open_slots",
    "patient_cancel_appointment_help",
    "search_patients",
    "general_health_question",
}


def base_intent(intent: str = "general_health_question") -> dict:
    """Return a consistent intent structure."""

    return {
        "intent": intent,
        "condition": None,
        "city": None,
        "age_lt": None,
        "age_gt": None,
        "name": None,
        "doctor_name": None,
        "time_preference": None,
        "date_preference": None,
    }


def extract_json(text: str) -> dict:
    """
    Extract a JSON object from an LLM response.

    The model is instructed to return JSON only, but this function
    also handles responses where the model surrounds JSON with
    additional text or markdown.
    """

    if not text:
        return base_intent()

    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else base_intent()
    except json.JSONDecodeError:
        pass

    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        parsed = json.loads(text[start:end])

        return parsed if isinstance(parsed, dict) else base_intent()

    except (ValueError, json.JSONDecodeError):
        return base_intent()


def validate_intent(intent_data: dict) -> dict:
    """
    Validate and normalize the intent returned by the LLM.
    """

    intent = intent_data.get("intent")

    if intent not in ALLOWED_INTENTS:
        return base_intent()

    validated = base_intent(intent)

    for field in validated:
        if field == "intent":
            continue

        if field in intent_data:
            validated[field] = intent_data[field]

    return validated


INTENT_SYSTEM_PROMPT = """
You are an AI tool-routing agent for a medical appointment system.

Convert the user's natural-language request into exactly ONE backend tool intent.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

Available intents:

- doctor_schedule_today
- doctor_all_appointments
- doctor_upcoming_appointments
- doctor_all_patients
- doctor_next_patient
- doctor_next_patient_history
- patient_my_appointments
- patient_available_doctors
- patient_open_slots
- patient_cancel_appointment_help
- search_patients
- general_health_question

Rules:

Doctor requests:

If the role is doctor and the user asks about their patients,
patient lists, assigned patients, patient details, or people under
their care, use doctor_all_patients.

If the role is doctor and the user asks about appointments generally,
use doctor_all_appointments.

If the role is doctor and the user asks about upcoming, future, or
next appointments, use doctor_upcoming_appointments.

If the role is doctor and the user asks about today's schedule,
use doctor_schedule_today.

If the role is doctor and the user asks about the next patient's
medical history, use doctor_next_patient_history.

If the role is doctor and the user asks to search or filter patients
by condition, disease, city, address, age, or name, use search_patients.

Patient requests:

If the role is patient and the user asks about their appointments,
use patient_my_appointments.

If the role is patient and the user asks for doctors or providers,
use patient_available_doctors.

If the role is patient and the user asks about available appointment
slots, use patient_open_slots.

If the role is patient and the user asks to cancel an appointment,
use patient_cancel_appointment_help.

For requests that do not match an application-specific tool,
use general_health_question.

Examples:

Doctor:
"show me my patients"

{
    "intent": "doctor_all_patients",
    "condition": null,
    "city": null,
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Doctor:
"show me my appointments"

{
    "intent": "doctor_all_appointments",
    "condition": null,
    "city": null,
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Doctor:
"show my upcoming appointments"

{
    "intent": "doctor_upcoming_appointments",
    "condition": null,
    "city": null,
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Doctor:
"show patients with diabetes"

{
    "intent": "search_patients",
    "condition": "diabetes",
    "city": null,
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Doctor:
"show patients above age 45"

{
    "intent": "search_patients",
    "condition": null,
    "city": null,
    "age_lt": null,
    "age_gt": 45,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Doctor:
"show patients in Dayton"

{
    "intent": "search_patients",
    "condition": null,
    "city": "Dayton",
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Patient:
"show me my appointments"

{
    "intent": "patient_my_appointments",
    "condition": null,
    "city": null,
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}

Patient:
"show me the list of doctors"

{
    "intent": "patient_available_doctors",
    "condition": null,
    "city": null,
    "age_lt": null,
    "age_gt": null,
    "name": null,
    "doctor_name": null,
    "time_preference": null,
    "date_preference": null
}
"""


def _call_mistral(messages, temperature=0):
    """Send a request to the Mistral API."""

    if not MISTRAL_API_KEY:
        raise RuntimeError(
            "MISTRAL_API_KEY environment variable is not configured."
        )

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    response = requests.post(
        MISTRAL_API_URL,
        headers=headers,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    data = response.json()

    choices = data.get("choices")

    if not choices:
        raise ValueError("Mistral API returned no choices.")

    return choices[0]["message"]["content"]


def detect_intent(user_message: str, role: str):
    """
    Determine which application tool should handle a user request.
    """

    if not user_message.strip():
        return base_intent()

    if role not in {"patient", "doctor", "admin"}:
        return base_intent()

    messages = [
        {
            "role": "system",
            "content": INTENT_SYSTEM_PROMPT.strip(),
        },
        {
            "role": "user",
            "content": (
                f"Role: {role}\n"
                f"Question: {user_message}"
            ),
        },
    ]

    try:
        content = _call_mistral(
            messages,
            temperature=0,
        )

        print(
            "INTENT CONTENT:",
            content,
            flush=True,
        )

        intent_data = extract_json(content)

        return validate_intent(intent_data)

    except (
        requests.RequestException,
        ValueError,
        RuntimeError,
    ) as exc:

        print(
            f"INTENT ERROR: {exc}",
            flush=True,
        )

        return base_intent()


AGENT_RESPONSE_SYSTEM_PROMPT = """
You are the assistant inside a medical appointment application.

Use only the database result provided to answer the user's question.

Do not invent appointments, patient records, medical history,
doctors, or other information.

Do not diagnose medical conditions or prescribe medication.

Present database results clearly and concisely.
"""


def format_agent_response(
    user_message: str,
    tool_result: str,
):
    """
    Convert a database tool result into a natural-language response.
    """

    if not tool_result:
        return "No information was returned by the application."

    messages = [
        {
            "role": "system",
            "content": AGENT_RESPONSE_SYSTEM_PROMPT.strip(),
        },
        {
            "role": "user",
            "content": (
                f"User asked: {user_message}\n\n"
                f"Database result:\n{tool_result}"
            ),
        },
    ]

    try:
        return _call_mistral(
            messages,
            temperature=0.3,
        )

    except (
        requests.RequestException,
        ValueError,
        RuntimeError,
    ) as exc:

        print(
            f"AGENT RESPONSE ERROR: {exc}",
            flush=True,
        )

        return tool_result

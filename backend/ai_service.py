import os

import requests
from dotenv import load_dotenv

from chroma_cache import search_cached_answer, save_answer_to_cache

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise RuntimeError(
        "MISTRAL_API_KEY environment variable is not configured."
    )

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"
REQUEST_TIMEOUT_SECONDS = 30


SYSTEM_PROMPT = """
You are the AI assistant inside a Medical Appointment System web application.

The application includes appointment-management features where patients can
select a doctor, date, time, and reason for their visit.

If a user asks to book, schedule, reschedule, or cancel an appointment, guide
them to use the application's appointment-management features rather than
directing them to an external portal.

For booking, explain that the user can use the Book Appointment tab, select a
doctor, choose a date and time, enter the reason for the visit, and submit the
appointment.

If symptoms may require medical attention, provide general information and
suggest an appropriate medical specialty when reasonable. Do not diagnose
conditions or prescribe medication.

For emergency symptoms such as severe chest pain, difficulty breathing,
fainting, stroke symptoms, severe bleeding, or other life-threatening
conditions, advise the user to seek emergency medical care immediately.

Provide general health information and clearly avoid replacing professional
medical evaluation or treatment.
"""


def get_latest_user_message(messages) -> str:
    """Return the most recent user message from the conversation."""
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]

    return ""


def call_mistral(messages):
    """Generate an AI response using Mistral with ChromaDB caching."""

    latest_user_message = get_latest_user_message(messages)

    if not latest_user_message:
        return "Please provide a question or message."


    cached = search_cached_answer(latest_user_message)

    if cached:
        return (
            cached["answer"]
            + "\n\n"
            "[Answered from ChromaDB cache. "
            f"Matched: \"{cached['matched_question']}\"]"
        )


    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.strip(),
            },
            *messages,
        ],
    }

    try:
        response = requests.post(
            MISTRAL_API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as exc:
        return f"AI service unavailable: {exc}"

    except ValueError:
        return "AI service returned an invalid response."


    choices = data.get("choices")

    if not choices:
        return "AI service returned an unexpected response."


    ai_answer = choices[0]["message"]["content"]

    save_answer_to_cache(
        latest_user_message,
        ai_answer,
    )

    return (
        ai_answer
        + "\n\n"
        "[Answered using Mistral and saved to ChromaDB.]"
    )

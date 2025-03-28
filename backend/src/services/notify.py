import os


def send_booking_confirmation(email: str, reference: str) -> dict:
    """SendGrid / SES hook — demo logs when API key absent."""
    if os.getenv("SENDGRID_API_KEY"):
        return {"provider": "sendgrid", "status": "queued", "to": email, "reference": reference}
    return {"provider": "log", "status": "skipped", "to": email, "reference": reference}

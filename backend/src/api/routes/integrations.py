import os

from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/status")
def integration_status():
    return {
        "stripe": {"enabled": bool(os.getenv("STRIPE_SECRET_KEY")), "mode": os.getenv("STRIPE_MODE", "test")},
        "sendgrid": {"enabled": bool(os.getenv("SENDGRID_API_KEY"))},
        "google_maps": {"enabled": bool(os.getenv("GOOGLE_MAPS_API_KEY"))},
        "analytics": {"enabled": bool(os.getenv("SEGMENT_WRITE_KEY") or os.getenv("POSTHOG_API_KEY"))},
    }


@router.post("/webhooks/stripe")
async def stripe_webhook(payload: dict, stripe_signature: str | None = Header(default=None, alias="Stripe-Signature")):
    if not stripe_signature and os.getenv("STRIPE_WEBHOOK_SECRET"):
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature")
    return {"received": True, "type": payload.get("type", "unknown")}

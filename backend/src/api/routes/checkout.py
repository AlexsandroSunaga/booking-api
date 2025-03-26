import os
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/checkout", tags=["checkout"])


class CheckoutSessionCreate(BaseModel):
    amount_cents: int = Field(ge=100)
    currency: str = Field(default="gbp", max_length=3)
    email: str
    description: str = "Transfer booking"


@router.post("/session")
def create_checkout_session(body: CheckoutSessionCreate):
    secret = os.getenv("STRIPE_SECRET_KEY")
    if secret:
        try:
            import stripe  # type: ignore

            stripe.api_key = secret
            session = stripe.checkout.Session.create(
                mode="payment",
                customer_email=body.email,
                line_items=[
                    {
                        "price_data": {
                            "currency": body.currency.lower(),
                            "unit_amount": body.amount_cents,
                            "product_data": {"name": body.description},
                        },
                        "quantity": 1,
                    }
                ],
                success_url=os.getenv("CHECKOUT_SUCCESS_URL", "http://localhost:3000/reservations?paid=1"),
                cancel_url=os.getenv("CHECKOUT_CANCEL_URL", "http://localhost:3000/quote"),
            )
            return {"session_id": session.id, "url": session.url, "provider": "stripe"}
        except Exception as e:
            raise HTTPException(502, f"Stripe error: {e}") from e

    sid = f"cs_demo_{uuid.uuid4().hex[:16]}"
    return {
        "session_id": sid,
        "url": f"/reservations?session={sid}&demo=1",
        "provider": "demo",
        "message": "Set STRIPE_SECRET_KEY for live Checkout",
    }

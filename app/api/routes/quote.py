from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.pricing import calculate_quote

router = APIRouter(prefix="/api/v1", tags=["quotes"])


class QuoteRequest(BaseModel):
    pickupLat: float
    pickupLng: float
    dropoffLat: float
    dropoffLng: float
    pickupDate: str = Field(description="YYYY-MM-DD")
    pickupTime: str = Field(description="HH:MM")
    isReturn: bool = False


@router.post("/quote")
def quote(body: QuoteRequest) -> dict:
    try:
        return calculate_quote(
            body.pickupLat,
            body.pickupLng,
            body.dropoffLat,
            body.dropoffLng,
            body.pickupDate,
            body.pickupTime,
            body.isReturn,
        )
    except ValueError as e:
        raise HTTPException(400, str(e)) from e

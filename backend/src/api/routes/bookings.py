from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/bookings", tags=["bookings"])

_STORE: list[dict] = []


class BookingCreate(BaseModel):
    destination: str = Field(min_length=2)
    travelers: int = Field(ge=1, le=20)
    start_date: str
    email: str


@router.get("")
def list_bookings():
    return {"items": _STORE, "total": len(_STORE)}


@router.post("")
def create_booking(body: BookingCreate):
    row = {
        "id": str(uuid4()),
        "reference": f"BK-{len(_STORE) + 1:05d}",
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    }
    _STORE.append(row)
    try:
        from src.services.notify import send_booking_confirmation

        send_booking_confirmation(body.email, row["reference"])
    except Exception:
        pass
    return row


@router.post("/{booking_id}/refund")
def refund_booking(booking_id: str):
    for row in _STORE:
        if row["id"] == booking_id:
            if row["status"] == "refunded":
                return {"id": booking_id, "status": "refunded", "message": "already refunded"}
            row["status"] = "refunded"
            row["refunded_at"] = datetime.now(timezone.utc).isoformat()
            return row
    raise HTTPException(404, "Booking not found")

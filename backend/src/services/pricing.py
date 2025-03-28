from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime

from src.config.manager import get_settings


@dataclass(frozen=True)
class VehicleType:
    slug: str
    name: str
    example: str
    passengers: int
    luggage: int
    hand_luggage: int
    multiplier: float


DEFAULT_VEHICLES = [
    VehicleType("saloon", "Saloon", "Toyota Camry", 3, 2, 2, 1.0),
    VehicleType("mpv", "MPV", "VW Sharan", 6, 4, 4, 1.25),
    VehicleType("executive", "Executive", "Mercedes E-Class", 3, 2, 2, 1.45),
]

MARKET_DEFAULTS = {
    "brazil": {
        "base_fare": 65.0,
        "per_mile": 3.5,
        "per_minute": 0.8,
        "minimum": 89.0,
        "airport_fee": 15.0,
        "currency": "BRL",
    },
    "uk": {
        "base_fare": 25.0,
        "per_mile": 1.85,
        "per_minute": 0.35,
        "minimum": 35.0,
        "airport_fee": 5.0,
        "currency": "GBP",
    },
    "default": {
        "base_fare": 30.0,
        "per_mile": 2.0,
        "per_minute": 0.4,
        "minimum": 40.0,
        "airport_fee": 8.0,
        "currency": "GBP",
    },
}


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def estimate_duration_minutes(km: float) -> int:
    avg_speed = 70 if km > 60 else 35
    return max(15, int(round((km / avg_speed) * 60 + 10)))


def is_night(hour: int, start: int = 22, end: int = 6) -> bool:
    if start > end:
        return hour >= start or hour < end
    return start <= hour < end


def day_surge(dt: datetime) -> float:
    if dt.weekday() == 4 and dt.hour >= 16:
        return 1.05
    if dt.weekday() in (5, 6):
        return 1.02
    return 1.0


def calculate_quote(
    pickup_lat: float,
    pickup_lng: float,
    dropoff_lat: float,
    dropoff_lng: float,
    pickup_date: str,
    pickup_time: str,
    is_return: bool = False,
) -> dict:
    settings = get_settings()
    rules = MARKET_DEFAULTS.get(settings.market.lower(), MARKET_DEFAULTS["default"])
    km = haversine_km(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
    miles = round(km * 0.621371, 1)
    minutes = estimate_duration_minutes(km)

    dt = datetime.fromisoformat(f"{pickup_date}T{pickup_time}")
    night_mult = 1.15 if is_night(dt.hour) else 1.0
    surge = day_surge(dt)

    vehicles_out = []
    for v in DEFAULT_VEHICLES:
        base = rules["base_fare"] + miles * rules["per_mile"] + minutes * rules["per_minute"]
        base = max(base, rules["minimum"]) + rules["airport_fee"]
        vehicle_price = round(base * v.multiplier * night_mult * surge, 2)
        total = round(vehicle_price * (2 if is_return else 1), 2)
        vehicles_out.append(
            {
                "vehicleTypeId": v.slug,
                "slug": v.slug,
                "name": v.name,
                "example": v.example,
                "passengers": v.passengers,
                "luggage": v.luggage,
                "handLuggage": v.hand_luggage,
                "basePrice": round(base, 2),
                "vehiclePrice": vehicle_price,
                "surgeMultiplier": surge,
                "totalPrice": total,
                "isReturn": bool(is_return),
            }
        )

    return {
        "distanceMiles": miles,
        "durationMinutes": minutes,
        "isNightRate": night_mult > 1,
        "surgeMultiplier": surge,
        "currency": rules.get("currency", settings.default_currency),
        "market": settings.market,
        "vehicles": vehicles_out,
    }

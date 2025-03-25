import pytest
from fastapi.testclient import TestClient

from app.main import app as legacy_app
from src.main import backend_app

QUOTE = {
    "pickupLat": 51.5074,
    "pickupLng": -0.1278,
    "dropoffLat": 51.47,
    "dropoffLng": -0.4543,
    "pickupDate": "2025-06-14",
    "pickupTime": "23:30",
    "isReturn": False,
}


@pytest.fixture(scope="module")
def legacy():
    return TestClient(legacy_app)


@pytest.fixture(scope="module")
def backend():
    return TestClient(backend_app)


@pytest.mark.parametrize("fixture_name", ["legacy", "backend"])
def test_health_and_quote_on_both_entries(request, fixture_name):
    client = request.getfixturevalue(fixture_name)
    assert client.get("/health").json()["status"] == "ok"
    body = client.post("/api/v1/quote", json=QUOTE).json()
    assert body["distanceMiles"] > 10
    assert [v["slug"] for v in body["vehicles"]] == ["saloon", "mpv", "executive"]
    # 23:30 is a night rate and 2025-06-14 is a Saturday
    assert body["isNightRate"] is True
    assert body["surgeMultiplier"] == 1.02


def test_return_trip_doubles_price(legacy):
    one_way = legacy.post("/api/v1/quote", json=QUOTE).json()["vehicles"][0]["totalPrice"]
    ret = legacy.post("/api/v1/quote", json={**QUOTE, "isReturn": True}).json()["vehicles"][0]["totalPrice"]
    assert ret == pytest.approx(one_way * 2, abs=0.01)


def test_quote_validation_errors(backend):
    assert backend.post("/api/v1/quote", json={"pickupLat": 1}).status_code == 422
    bad_date = backend.post("/api/v1/quote", json={**QUOTE, "pickupDate": "not-a-date"})
    assert bad_date.status_code == 400


def test_booking_create_list_refund(backend):
    payload = {
        "destination": "Heathrow Terminal 5",
        "travelers": 2,
        "start_date": "2025-06-14",
        "email": "guest@example.com",
    }
    created = backend.post("/api/v1/bookings", json=payload)
    assert created.status_code == 200
    booking = created.json()
    assert booking["status"] == "confirmed" and booking["reference"].startswith("BK-")
    assert backend.get("/api/v1/bookings").json()["total"] >= 1

    refunded = backend.post(f"/api/v1/bookings/{booking['id']}/refund")
    assert refunded.status_code == 200 and refunded.json()["status"] == "refunded"


def test_booking_validation_and_missing_refund(backend):
    assert backend.post("/api/v1/bookings", json={"destination": "X", "travelers": 0}).status_code == 422
    assert backend.post("/api/v1/bookings/does-not-exist/refund").status_code == 404


def test_checkout_demo_session_and_integrations(backend, monkeypatch):
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    r = backend.post(
        "/api/v1/checkout/session",
        json={"amount_cents": 8500, "currency": "gbp", "email": "guest@example.com"},
    )
    assert r.status_code == 200 and r.json()["provider"] == "demo"
    assert backend.post("/api/v1/checkout/session", json={"amount_cents": 5, "email": "a@b.co"}).status_code == 422
    assert backend.get("/api/v1/integrations/status").json()["stripe"]["enabled"] is False

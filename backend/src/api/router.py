from fastapi import APIRouter

from src.api.routes import quote, bookings, integrations, checkout

api_router = APIRouter()
api_router.include_router(quote.router)
api_router.include_router(bookings.router)
api_router.include_router(integrations.router)
api_router.include_router(checkout.router)



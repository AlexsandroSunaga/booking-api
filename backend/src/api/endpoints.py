from fastapi import APIRouter, FastAPI


def attach_routes(app: FastAPI, router: APIRouter, prefix: str) -> None:
    app.include_router(router, prefix=prefix)

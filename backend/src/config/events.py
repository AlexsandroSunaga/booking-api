from collections.abc import Callable

from fastapi import FastAPI


def create_start_app_handler(app: FastAPI, on_startup: Callable) -> Callable:
    async def _startup() -> None:
        await on_startup()

    app.add_event_handler("startup", _startup)
    return _startup

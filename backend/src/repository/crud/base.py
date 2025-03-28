from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.table import Base

ModelT = TypeVar("ModelT", bound=Base)


class CRUDBase(Generic[ModelT]):
    def __init__(self, model: type[ModelT]):
        self.model = model

    async def get(self, db: AsyncSession, pk: int) -> ModelT | None:
        return await db.get(self.model, pk)

    async def list(self, db: AsyncSession, limit: int = 100) -> list[ModelT]:
        result = await db.execute(select(self.model).limit(limit))
        return list(result.scalars().all())

from src.repository.database import engine
from src.repository.table import Base


async def init_database_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

"""Import all ORM models here for Alembic autogenerate."""

from src.repository.table import Base

# noqa: F401 — models imported in product-specific repository/base override

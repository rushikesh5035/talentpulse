from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Create async engine (the connection pool)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG, # prints sql queries  in terminal for debug
)

# Sessionn factory
# each request gets its own session created from this factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # # Don't expire objects after commit (safer for async)
)

# Base class for all our ORM models
# Every model (User, Candidate, Job) will inherit from this
class Base(DeclarativeBase):
    pass

# Dependency: yields a DB session per request
# Used in routes as: db: AsyncSession = Depends(get_db)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session             # ← hand session to the route handler
            await session.commit()    # ← auto-commit on success
        except Exception:
            await session.rollback()  # ← auto-rollback on any error
            raise
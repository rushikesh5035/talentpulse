from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch a user from the database by email."""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

async def create_user(
    db: AsyncSession,
    email: str,
    name: str,
    password: str,
    role: str = "candidate",
) -> User:
    """Create a new user in the database."""
    user = User(
        email=email,
        name=name,
        hashed_password=get_password_hash(password),
        role=role,
        is_active=True
    )

    db.add(user)
    
    await db.flush() # writes to DB but doesn't commit yet (get_db handles commit)
    
    return user
    
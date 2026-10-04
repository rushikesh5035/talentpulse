"""
Seed script: Populates the database with initial users.
Run with: uv run python -m app.seed
"""

import asyncio
from app.core.database import AsyncSessionLocal, engine, Base
from app.services.user_service import get_user_by_email, create_user


# Define seed users
SEED_USERS = [
    {
        "email": "admin@talentpulse.com",
        "name": "Admin User",
        "password": "admin123",
        "role": "admin",
    },
    {
        "email": "recruiter@talentpulse.com",
        "name": "Recruiter User",
        "password": "recruiter123",
        "role": "recruiter",
    },
    {
        "email": "candidate@talentpulse.com",
        "name": "Test Candidate",
        "password": "candidate123",
        "role": "candidate",
    },
]


async def seed():
    print("🌱 Starting database seed...")

    async with AsyncSessionLocal() as db:
        for user_data in SEED_USERS:
            # Check if user already exists (avoid duplicates)
            existing = await get_user_by_email(db, user_data["email"])
            if existing:
                print(f"  ⏭️  {user_data['email']} already exists, skipping.")
                continue

            user = await create_user(
                db=db,
                email=user_data["email"],
                name=user_data["name"],
                password=user_data["password"],
                role=user_data["role"],
            )
            print(f"  ✅ Created: {user.email} (role: {user.role})")

        await db.commit()

    print("🌱 Seed complete!")


if __name__ == "__main__":
    asyncio.run(seed())

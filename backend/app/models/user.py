import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    # Primary Key — UUID string
    id : Mapped[str] = mapped_column(
        String(36), 
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Identity
    email : Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    name : Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    hashed_password : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Role & Permissions
    role : Mapped[str] = mapped_column(
        String(50),
        default="candidate",
        nullable=False
    )

    # Account Status
    is_active : Mapped[bool] = mapped_column(
        Boolean, 
        default=True
    )

    # Timestamps
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) 
    )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
    
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Meta(Base):
    __tablename__ = "meta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    master_password: Mapped[str] = mapped_column(String, nullable=False)


class Password(Base):
    __tablename__ = "passwords"
    __table_args__ = (UniqueConstraint("username", "platform", "meta_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meta_id: Mapped[int] = mapped_column(Integer, ForeignKey("meta.id"), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    platform: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class Position(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "positions"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship(back_populates="position")


class Workplace(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "workplaces"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    photo_s3_key: Mapped[str | None] = mapped_column(String(512))

    users: Mapped[list["User"]] = relationship(back_populates="workplace")


class UserStatus(UUIDPKMixin, Base):
    __tablename__ = "user_statuses"

    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active_system: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="status")


class User(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(64))
    schedule: Mapped[str | None] = mapped_column(String(255))

    position_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("positions.id", ondelete="SET NULL")
    )
    workplace_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("workplaces.id", ondelete="SET NULL"),
        index=True,
    )
    status_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("user_statuses.id"), nullable=False, index=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )

    position: Mapped[Position | None] = relationship(back_populates="users")
    workplace: Mapped[Workplace | None] = relationship(back_populates="users")
    status: Mapped[UserStatus] = relationship(back_populates="users")

    roles: Mapped[list["UserRole"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    permissions: Mapped[list["UserPermission"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    visibility: Mapped["InfoCardVisibility | None"] = relationship(  # noqa: F821
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    reserve: Mapped["PersonnelReserve | None"] = relationship(  # noqa: F821
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class InfoCardVisibility(Base):
    __tablename__ = "info_card_visibility"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    visible_to_all: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    granted_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped[User] = relationship(back_populates="visibility", foreign_keys=[user_id])


class PersonnelReserve(Base):
    __tablename__ = "personnel_reserve"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    fired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    added_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    notes: Mapped[str | None] = mapped_column(Text)
    is_restored: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    restored_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="reserve", foreign_keys=[user_id])
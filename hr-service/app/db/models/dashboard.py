from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import UUIDPKMixin


class DashboardPeriod(UUIDPKMixin, Base):
    __tablename__ = "dashboard_periods"
    __table_args__ = (UniqueConstraint("period_start", "period_end"),)

    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    calculated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    stats: Mapped[list["DashboardStat"]] = relationship(
        back_populates="period", cascade="all, delete-orphan"
    )


class DashboardStat(UUIDPKMixin, Base):
    __tablename__ = "dashboard_stats"
    __table_args__ = (UniqueConstraint("period_id", "creator_id"),)

    period_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dashboard_periods.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    creator_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    period: Mapped[DashboardPeriod] = relationship(back_populates="stats")
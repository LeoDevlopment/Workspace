from uuid import UUID

from sqlalchemy import BigInteger, Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class Document(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    owner_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    owner_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(128))
    size: Mapped[int | None] = mapped_column(BigInteger)
    uploaded_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    access: Mapped[list["DocumentAccess"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class DocumentAccess(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "document_access"
    __table_args__ = (UniqueConstraint("document_id", "subject_type", "subject_id"),)

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    subject_type: Mapped[str] = mapped_column(String(16), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    can_view: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    granted_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )

    document: Mapped[Document] = relationship(back_populates="access")


class WorkplaceDocumentAccess(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "workplace_document_access"
    __table_args__ = (UniqueConstraint("workplace_id", "subject_type", "subject_id"),)

    workplace_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("workplaces.id", ondelete="CASCADE"), nullable=False
    )
    subject_type: Mapped[str] = mapped_column(String(16), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    can_view: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    granted_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
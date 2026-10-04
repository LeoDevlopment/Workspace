from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import Perm
from app.core.permissions_cache import get_user_permissions
from app.db.models import (
    Document,
    DocumentAccess,
    InfoCardVisibility,
    User,
    UserStatus,
    WorkplaceDocumentAccess,
)


FIRED_CODE = "fired"


# ---------- Пользователи ----------

async def can_view_user_card(session: AsyncSession, actor: User, target: User) -> bool:
    if actor.id == target.id:
        return True

    perms = await get_user_permissions(session, actor.id)

    if Perm.USERS_VIEW_ALL.value in perms:
        return True

    # уволенные
    status = await session.get(UserStatus, target.status_id)
    if status and status.code == FIRED_CODE:
        return Perm.USERS_VIEW_FIRED.value in perms

    # публичная карточка
    visibility = await session.get(InfoCardVisibility, target.id)
    if visibility and visibility.visible_to_all:
        return True

    # коллеги по месту работы
    if (
        Perm.USERS_VIEW_COLLEAGUES.value in perms
        and actor.workplace_id is not None
        and actor.workplace_id == target.workplace_id
    ):
        return True

    return False


# ---------- Документы ----------

async def _subject_ids(actor: User, actor_role_ids: list[UUID]) -> dict[str, list[UUID]]:
    return {"user": [actor.id], "role": actor_role_ids}


async def _actor_subject_ids(session: AsyncSession, actor: User) -> tuple[list[UUID], list[UUID]]:
    role_stmt = select(UserRoleRoleId := None)
    # получаем id ролей пользователя
    from app.db.models import UserRole

    roles = (await session.scalars(select(UserRole.role_id).where(UserRole.user_id == actor.id))).all()
    return [actor.id], list(roles)


async def _has_document_access(
    session: AsyncSession,
    doc: Document,
    actor_user_ids: list[UUID],
    actor_role_ids: list[UUID],
) -> bool:
    stmt = select(DocumentAccess).where(
        DocumentAccess.document_id == doc.id,
        DocumentAccess.can_view.is_(True),
    )
    rows = (await session.scalars(stmt)).all()
    for row in rows:
        if row.subject_type == "user" and row.subject_id in actor_user_ids:
            return True
        if row.subject_type == "role" and row.subject_id in actor_role_ids:
            return True
    return False


async def _has_workplace_access(
    session: AsyncSession,
    workplace_id: UUID,
    actor_user_ids: list[UUID],
    actor_role_ids: list[UUID],
) -> bool:
    stmt = select(WorkplaceDocumentAccess).where(
        WorkplaceDocumentAccess.workplace_id == workplace_id,
        WorkplaceDocumentAccess.can_view.is_(True),
    )
    rows = (await session.scalars(stmt)).all()
    for row in rows:
        if row.subject_type == "user" and row.subject_id in actor_user_ids:
            return True
        if row.subject_type == "role" and row.subject_id in actor_role_ids:
            return True
    return False


async def can_view_document(session: AsyncSession, actor: User, doc: Document) -> bool:
    if doc.is_deleted:
        return False

    perms = await get_user_permissions(session, actor.id)

    if Perm.DOCUMENTS_VIEW_ALL.value in perms:
        return True

    actor_user_ids, actor_role_ids = await _actor_subject_ids(session, actor)

    if doc.owner_type == "user":
        if doc.owner_id == actor.id and Perm.DOCUMENTS_VIEW_OWN.value in perms:
            return True
        return await _has_document_access(session, doc, actor_user_ids, actor_role_ids)

    if doc.owner_type == "workplace":
        if await _has_workplace_access(session, doc.owner_id, actor_user_ids, actor_role_ids):
            return True
        return await _has_document_access(session, doc, actor_user_ids, actor_role_ids)

    return False


async def filter_accessible_documents(
    session: AsyncSession, actor: User, documents: list[Document]
) -> list[Document]:
    result: list[Document] = []
    for doc in documents:
        if await can_view_document(session, actor, doc):
            result.append(doc)
    return result


# ---------- Оценки и комментарии ----------

async def can_view_rating(session: AsyncSession, actor: User) -> bool:
    perms = await get_user_permissions(session, actor.id)
    return Perm.RATINGS_VIEW.value in perms


async def can_view_comment(session: AsyncSession, actor: User) -> bool:
    perms = await get_user_permissions(session, actor.id)
    return Perm.COMMENTS_VIEW.value in perms


async def can_view_personnel_reserve(session: AsyncSession, actor: User) -> bool:
    perms = await get_user_permissions(session, actor.id)
    return Perm.PERSONNEL_RESERVE_VIEW.value in perms
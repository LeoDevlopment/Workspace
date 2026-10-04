import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import redis_client
from app.db.models import Permission, RolePermission, UserPermission, UserRole

PERMS_TTL = 300  # 5 минут


def _key(user_id: str) -> str:
    return f"perms:{user_id}"


async def load_permissions_from_db(session: AsyncSession, user_id) -> set[str]:
    # права ролей
    role_stmt = (
        select(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .where(UserRole.user_id == user_id)
    )
    codes = set((await session.scalars(role_stmt)).all())

    # индивидуальные права
    indiv_stmt = (
        select(Permission.code, UserPermission.effect)
        .join(UserPermission, UserPermission.permission_id == Permission.id)
        .where(UserPermission.user_id == user_id)
    )
    for code, effect in (await session.execute(indiv_stmt)).all():
        if effect == "allow":
            codes.add(code)
        elif effect == "deny":
            codes.discard(code)

    return codes


async def get_user_permissions(session: AsyncSession, user_id) -> set[str]:
    raw = await redis_client.get(_key(str(user_id)))
    if raw is not None:
        return set(json.loads(raw))
    perms = await load_permissions_from_db(session, user_id)
    await redis_client.set(_key(str(user_id)), json.dumps(sorted(perms)), ex=PERMS_TTL)
    return perms


async def invalidate_user_permissions(user_id) -> None:
    await redis_client.delete(_key(str(user_id)))
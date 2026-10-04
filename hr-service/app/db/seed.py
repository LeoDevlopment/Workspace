import asyncio
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.permissions import DEFAULT_USER_PERMISSIONS, Perm, SYSTEM_ROLE_ADMIN, SYSTEM_ROLE_USER
from app.core.security import hash_password
from app.db.models import (
    DashboardPeriod,
    Permission,
    Role,
    RolePermission,
    User,
    UserRole,
    UserStatus,
)
from app.db.session import SessionLocal


STATUSES = [
    ("employed", "В штате"),
    ("fired", "Уволен"),
    ("vacation", "Отпуск"),
    ("sick", "Больничный"),
]


async def _seed_statuses(session: AsyncSession) -> dict[str, UserStatus]:
    result: dict[str, UserStatus] = {}
    for code, name in STATUSES:
        st = await session.scalar(select(UserStatus).where(UserStatus.code == code))
        if st is None:
            st = UserStatus(code=code, name=name, is_active_system=(code == "employed"))
            session.add(st)
        result[code] = st
    await session.flush()
    return result


async def _seed_permissions(session: AsyncSession) -> dict[str, Permission]:
    perms: dict[str, Permission] = {}
    for perm in Perm:
        p = await session.scalar(select(Permission).where(Permission.code == perm.value))
        if p is None:
            p = Permission(code=perm.value, description=perm.value)
            session.add(p)
        perms[perm.value] = p
    await session.flush()
    return perms


async def _seed_roles(session: AsyncSession, perms: dict[str, Permission]) -> dict[str, Role]:
    roles: dict[str, Role] = {}

    admin_role = await session.scalar(select(Role).where(Role.name == SYSTEM_ROLE_ADMIN))
    if admin_role is None:
        admin_role = Role(name=SYSTEM_ROLE_ADMIN, is_system=True, description="Системный администратор")
        session.add(admin_role)
        await session.flush()
        for p in perms.values():
            session.add(RolePermission(role_id=admin_role.id, permission_id=p.id))
    roles[SYSTEM_ROLE_ADMIN] = admin_role

    user_role = await session.scalar(select(Role).where(Role.name == SYSTEM_ROLE_USER))
    if user_role is None:
        user_role = Role(name=SYSTEM_ROLE_USER, is_system=True, description="Пользователь")
        session.add(user_role)
        await session.flush()
        for code in DEFAULT_USER_PERMISSIONS:
            session.add(RolePermission(role_id=user_role.id, permission_id=perms[code.value].id))
    roles[SYSTEM_ROLE_USER] = user_role

    return roles


async def _seed_bootstrap_admin(
    session: AsyncSession, roles: dict[str, Role], statuses: dict[str, UserStatus]
) -> None:
    existing = await session.scalar(
        select(User).where(User.login == settings.BOOTSTRAP_ADMIN_LOGIN)
    )
    if existing is not None:
        return

    admin = User(
        login=settings.BOOTSTRAP_ADMIN_LOGIN,
        full_name="Администратор",
        password_hash=hash_password(settings.BOOTSTRAP_ADMIN_PASSWORD),
        status_id=statuses["employed"].id,
        is_active=True,
        must_change_password=True,
    )
    session.add(admin)
    await session.flush()
    session.add(UserRole(user_id=admin.id, role_id=roles[SYSTEM_ROLE_ADMIN].id))


async def _seed_active_dashboard_period(session: AsyncSession) -> None:
    today = date.today()
    period_start = today.replace(day=1)
    if period_start.month == 12:
        period_end = period_start.replace(year=period_start.year + 1, month=1)
    else:
        period_end = period_start.replace(month=period_start.month + 1)
    from datetime import timedelta

    period_end = period_end - timedelta(days=1)

    existing = await session.scalar(
        select(DashboardPeriod).where(DashboardPeriod.status == "active")
    )
    if existing is None:
        session.add(
            DashboardPeriod(period_start=period_start, period_end=period_end, status="active")
        )


async def seed() -> None:
    async with SessionLocal() as session:
        statuses = await _seed_statuses(session)
        perms = await _seed_permissions(session)
        roles = await _seed_roles(session, perms)
        await _seed_bootstrap_admin(session, roles, statuses)
        await _seed_active_dashboard_period(session)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
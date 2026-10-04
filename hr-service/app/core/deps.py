from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.permissions import Perm
from app.core.permissions_cache import get_user_permissions
from app.core.session import delete_session, get_session, refresh_session
from app.db.models import User
from app.db.session import get_session as db_session


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(db_session),
) -> User:
    session_id = request.cookies.get(settings.COOKIE_NAME)
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Не авторизован")

    sess = await get_session(session_id)
    if not sess:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Сессия истекла")

    user = await session.get(User, UUID(sess["user_id"]))
    if user is None or not user.is_active:
        await delete_session(session_id)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Учётная запись недоступна")

    await refresh_session(session_id)
    request.state.session_id = session_id
    return user


def require_permission(perm: Perm):
    async def _checker(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_session),
    ) -> User:
        perms = await get_user_permissions(session, user.id)
        if perm.value not in perms:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Недостаточно прав")
        return user

    return _checker


def require_any_permission(*perms: Perm):
    allowed = {p.value for p in perms}

    async def _checker(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_session),
    ) -> User:
        user_perms = await get_user_permissions(session, user.id)
        if not (user_perms & allowed):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Недостаточно прав")
        return user

    return _checker
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import (
    generate_session_id,
    hash_password,
    validate_password_strength,
    verify_password,
)
from app.core.session import (
    create_session,
    delete_all_user_sessions,
    delete_session,
    redis_client,
)
from app.db.models import User
from app.db.session import get_session as db_session

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

LOGIN_RATE_LIMIT = 10
LOGIN_RATE_WINDOW = 300


async def _rate_limit_check(login: str) -> bool:
    key = f"login_attempts:{login.lower()}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, LOGIN_RATE_WINDOW)
    return count <= LOGIN_RATE_LIMIT


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, next: str | None = None):
    return templates.TemplateResponse(
        "auth/login.html", {"request": request, "next": next, "error": None}
    )


@router.post("/login")
async def login(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    next: str | None = Form(default=None),
    session: AsyncSession = Depends(db_session),
):
    if not await _rate_limit_check(login):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Слишком много попыток. Попробуйте позже.", "next": next},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    user = await session.scalar(select(User).where(User.login == login))
    if user is None or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Неверный логин или пароль", "next": next},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Учётная запись деактивирована", "next": next},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    await redis_client.delete(f"login_attempts:{login.lower()}")

    session_id = generate_session_id()
    await create_session(
        session_id,
        str(user.id),
        ip=request.client.host if request.client else None,
        ua=request.headers.get("user-agent"),
    )

    redirect_to = "/auth/change-password" if user.must_change_password else (next or "/")
    response = RedirectResponse(redirect_to, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        settings.COOKIE_NAME,
        session_id,
        max_age=settings.SESSION_TTL_SECONDS,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return response


@router.post("/logout")
async def logout(request: Request):
    session_id = request.cookies.get(settings.COOKIE_NAME)
    if session_id:
        await delete_session(session_id)
    response = RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(settings.COOKIE_NAME, path="/")
    return response


@router.get("/change-password", response_class=HTMLResponse)
async def change_password_form(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "auth/change_password.html",
        {"request": request, "user": user, "error": None, "forced": user.must_change_password},
    )


@router.post("/change-password")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_session),
):
    def render_error(msg: str):
        return templates.TemplateResponse(
            "auth/change_password.html",
            {"request": request, "user": user, "error": msg, "forced": user.must_change_password},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not verify_password(current_password, user.password_hash):
        return render_error("Текущий пароль введён неверно")

    if new_password != confirm_password:
        return render_error("Пароли не совпадают")

    try:
        validate_password_strength(new_password)
    except ValueError as e:
        return render_error(str(e))

    user.password_hash = hash_password(new_password)
    user.must_change_password = False
    await session.commit()

    current_sid = request.cookies.get(settings.COOKIE_NAME)
    await delete_all_user_sessions(str(user.id), except_session_id=current_sid)

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
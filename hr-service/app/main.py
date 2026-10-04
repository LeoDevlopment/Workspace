from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth as auth_api
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_api.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    wants_html = "text/html" in request.headers.get("accept", "")
    if exc.status_code == status.HTTP_401_UNAUTHORIZED and wants_html:
        next_path = request.url.path
        return RedirectResponse(
            f"/auth/login?next={next_path}", status_code=status.HTTP_302_FOUND
        )
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def index():
    return RedirectResponse("/users/me", status_code=status.HTTP_302_FOUND)
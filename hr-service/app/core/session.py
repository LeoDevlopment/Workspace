import json
from datetime import datetime, timezone

import redis.asyncio as aioredis

from app.core.config import settings

redis_client: aioredis.Redis = aioredis.from_url(
    settings.redis_url, encoding="utf-8", decode_responses=True
)


def _session_key(session_id: str) -> str:
    return f"session:{session_id}"


def _user_sessions_key(user_id: str) -> str:
    return f"user_sessions:{user_id}"


async def create_session(session_id: str, user_id: str, ip: str | None, ua: str | None) -> None:
    payload = {
        "user_id": user_id,
        "ip": ip,
        "ua": ua,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.set(_session_key(session_id), json.dumps(payload), ex=settings.SESSION_TTL_SECONDS)
        pipe.sadd(_user_sessions_key(user_id), session_id)
        pipe.expire(_user_sessions_key(user_id), settings.SESSION_TTL_SECONDS)
        await pipe.execute()


async def get_session(session_id: str) -> dict | None:
    raw = await redis_client.get(_session_key(session_id))
    return json.loads(raw) if raw else None


async def refresh_session(session_id: str) -> None:
    await redis_client.expire(_session_key(session_id), settings.SESSION_TTL_SECONDS)


async def delete_session(session_id: str) -> None:
    raw = await redis_client.get(_session_key(session_id))
    if raw:
        data = json.loads(raw)
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.delete(_session_key(session_id))
            pipe.srem(_user_sessions_key(data["user_id"]), session_id)
            await pipe.execute()


async def delete_all_user_sessions(user_id: str, except_session_id: str | None = None) -> None:
    ids = await redis_client.smembers(_user_sessions_key(user_id))
    async with redis_client.pipeline(transaction=True) as pipe:
        for sid in ids:
            if except_session_id and sid == except_session_id:
                continue
            pipe.delete(_session_key(sid))
            pipe.srem(_user_sessions_key(user_id), sid)
        await pipe.execute()
from collections.abc import Generator

import redis

from app.config import settings


def get_redis() -> Generator[redis.Redis, None, None]:
    client = redis.from_url(settings.redis_url, decode_responses=True)
    try:
        yield client
    finally:
        client.close()

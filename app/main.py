from collections.abc import Callable
from typing import cast

from fastapi import Depends, FastAPI
import redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db
from app.redis_client import get_redis

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/db-ping")
def db_ping(db: Session = Depends(get_db)):
    one = db.execute(text("SELECT 1")).scalar_one()
    return {"ok": True, "select_1": one}


@app.get("/redis-ping")
def redis_ping(r: redis.Redis = Depends(get_redis)):
    # Yes, even when using a shared pool, you use the dependency the same way.
    pong = cast(Callable[[], bool], r.ping)()
    return {"ok": True, "ping": pong}

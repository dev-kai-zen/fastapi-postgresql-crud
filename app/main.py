from fastapi import FastAPI, Depends
from app.db import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/db-ping")
def db_ping(db: Session = Depends(get_db)):
    one = db.execute(text("SELECT 1")).scalar_one()
    return {"ok": True, "select_1": one}

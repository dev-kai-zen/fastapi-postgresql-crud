from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.features.crud.service import crud_service as svc
from app.features.crud.schemas.items_schema import ItemCreate, ItemRead, ItemUpdate


def list_items(db: Session, *, skip: int = 0, limit: int = 100) -> list[ItemRead]:
    return svc.list_items(db, skip=skip, limit=limit)


def read_item(db: Session, item_id: int) -> ItemRead:
    item = svc.get_item(db, item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


def create_item(db: Session, data: ItemCreate) -> ItemRead:
    return svc.create_item(db, data)


def update_item(db: Session, item_id: int, data: ItemUpdate) -> ItemRead:
    item = svc.update_item(db, item_id, data)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


def delete_item(db: Session, item_id: int) -> None:
    if not svc.delete_item(db, item_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")

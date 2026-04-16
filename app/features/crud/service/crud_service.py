from sqlalchemy.orm import Session

from app.features.crud.repository import crud_repository as repo
from app.features.crud.schemas.items_schema import ItemCreate, ItemRead, ItemUpdate


def list_items(db: Session, *, skip: int = 0, limit: int = 100) -> list[ItemRead]:
    rows = repo.list_items(db, skip=skip, limit=limit)
    return [ItemRead.model_validate(r) for r in rows]


def get_item(db: Session, item_id: int) -> ItemRead | None:
    row = repo.get_by_id(db, item_id)
    if row is None:
        return None
    return ItemRead.model_validate(row)


def create_item(db: Session, data: ItemCreate) -> ItemRead:
    row = repo.create(db, data)
    return ItemRead.model_validate(row)


def update_item(db: Session, item_id: int, data: ItemUpdate) -> ItemRead | None:
    row = repo.update(db, item_id, data)
    if row is None:
        return None
    return ItemRead.model_validate(row)


def delete_item(db: Session, item_id: int) -> bool:
    return repo.delete(db, item_id)

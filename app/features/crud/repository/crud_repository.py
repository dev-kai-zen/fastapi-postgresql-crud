from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.crud.models.items_model import Item
from app.features.crud.schemas.items_schema import ItemCreate, ItemUpdate


def get_by_id(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)


def list_items(db: Session, *, skip: int = 0, limit: int = 100) -> list[Item]:
    stmt = select(Item).order_by(Item.id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create(db: Session, data: ItemCreate) -> Item:
    row = Item(title=data.title, description=data.description)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, item_id: int, data: ItemUpdate) -> Item | None:
    row = get_by_id(db, item_id)
    if row is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete(db: Session, item_id: int) -> bool:
    row = get_by_id(db, item_id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True

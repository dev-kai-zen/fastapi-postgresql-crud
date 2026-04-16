from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.features.crud.controller import crud_controller as ctrl
from app.features.crud.schemas.items_schema import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemRead])
def list_items(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
) -> list[ItemRead]:
    return ctrl.list_items(db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    return ctrl.read_item(db, item_id)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    return ctrl.create_item(db, data)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int, data: ItemUpdate, db: Session = Depends(get_db)
) -> ItemRead:
    return ctrl.update_item(db, item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    ctrl.delete_item(db, item_id)

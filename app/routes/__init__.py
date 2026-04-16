from fastapi import APIRouter

from app.features.crud.routes.crud_routes import router as crud_router
from app.features.app_testing.app_testing_routes import router as routes_test_router


def register_v1_routes() -> APIRouter:
    router = APIRouter()
    router.include_router(routes_test_router)
    router.include_router(crud_router)
    return router

from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.note import router as note_router
from .endpoints.user import router as user_router

router = APIRouter(prefix="/v1")

router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(auth_router, prefix="", tags=["Auth"])
router.include_router(note_router, prefix="/note", tags=["Note"])

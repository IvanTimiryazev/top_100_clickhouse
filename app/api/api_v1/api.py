from fastapi import APIRouter

from app.api.api_v1.endpoints import words

api_router = APIRouter()

api_router.include_router(words.router, tags=["Words"])
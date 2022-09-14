from fastapi import APIRouter

from app.api.endpoints import artists

api_router = APIRouter()


api_router.include_router(artists.router, prefix="/artists", tags=["artists"])

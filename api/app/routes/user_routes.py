from fastapi import APIRouter
from app.services.user_service import sync_user, user_recommendations

router = APIRouter()

@router.get("/sync-user")
async def sync_user_route(username: str, password: str):
    return await sync_user(username, password)

@router.get("/user-recommendations")
async def user_recommendations_route(name: str):
    return await user_recommendations(name)

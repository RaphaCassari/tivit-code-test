from fastapi import APIRouter
from app.services.admin_service import sync_admin, admin_recommendations

router = APIRouter()

@router.get("/sync-admin")
async def sync_admin_route(username: str, password: str):
    return await sync_admin(username, password)

@router.get("/admin-recommendations")
async def admin_recommendations_route(name: str):
    return await admin_recommendations(name)

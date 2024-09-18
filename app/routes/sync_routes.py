from fastapi import APIRouter, Depends
from app.database.neo4j_service import Neo4jService

sync_router = APIRouter()


@sync_router.post("/sync/user")
def sync_user_data(user_data: dict):
    neo4j_service = Neo4jService(
        uri="bolt://localhost:7687", user="neo4j", password="password")
    neo4j_service.save_user_data(user_data)
    neo4j_service.close()
    return {"message": "User data synced successfully"}


@sync_router.post("/sync/admin")
def sync_admin_data(admin_data: dict):
    neo4j_service = Neo4jService(
        uri="bolt://localhost:7687", user="neo4j", password="password")
    neo4j_service.save_admin_data(admin_data)
    neo4j_service.close()
    return {"message": "Admin data synced successfully"}

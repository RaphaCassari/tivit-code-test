from fastapi import APIRouter, Depends
from app.database.neo4j_service import Neo4jService

recommendation_router = APIRouter()


@recommendation_router.get("/recommendations/{name}")
def get_recommendations(name: str):
    neo4j_service = Neo4jService(
        uri="bolt://localhost:7687", user="neo4j", password="password")
    recommendations = neo4j_service.get_recommendations(name)
    neo4j_service.close()
    return {
        "message": f"Recommendations for {name}",
        "recommendations": recommendations
    }

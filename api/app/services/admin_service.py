from app.database.neo4j_client import Neo4jClient
from app.utils.auth import get_fake_token

async def sync_admin(username: str, password: str):
    token = get_fake_token(username, password)
    client = Neo4jClient()
    client.close()
    return {"status": "success"}

async def admin_recommendations(name: str):
    client = Neo4jClient()
    recommendations = client.get_admin_recommendations(name)
    client.close()
    return {"recommendations": recommendations}

from app.database.neo4j_client import Neo4jClient
from app.utils.auth import get_fake_token
from fastapi import HTTPException
import requests
import os

FAKE_API_URL = os.getenv("FAKE_API_URL", "http://localhost:8000")

# Função para sincronizar usuário e salvar no banco Neo4j


async def sync_user(username: str, password: str):
    # Obtém token fake para o usuário
    token = get_fake_token(username, password)

    # Faz uma requisição à API fake para obter os dados do usuário
    response = requests.get(f"{FAKE_API_URL}/user",
                            headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        # Se sucesso, salva o usuário no banco Neo4j
        user_data = response.json()["data"]
        client = Neo4jClient()
        client.save_user(user_data)
        client.close()
        return {"status": "success", "data": user_data}
    else:
        # Se a API retornar erro, lança uma exceção
        raise HTTPException(
            status_code=response.status_code, detail=response.text)

# Função para obter recomendações para o usuário a partir do nome


async def user_recommendations(name: str):
    client = Neo4jClient()
    recommendations = client.get_user_recommendations(name)
    client.close()
    return {"recommendations": recommendations}

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
from neo4j import GraphDatabase
from jose import JWTError, jwt
from datetime import datetime, timedelta
from urllib.parse import quote, unquote
import os

from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do .env

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")


# Configurações Neo4j
#NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://a4051114.databases.neo4j.io")
#NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
#NEO4J_PASSWORD = os.getenv(
#    "NEO4J_PASSWORD", "SRr0ul04xAaSdhOkmCvgFHjyZKaYFNOZXiE03JZXptA")

# Configuração da API Fake
FAKE_API_URL = os.getenv("FAKE_API_URL", "http://localhost:8000")

# Configurações do JWT
#SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Configuração de CORS
origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir origens específicas
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cliente Neo4j


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def save_user(self, user_data):
        with self.driver.session() as session:
            session.write_transaction(self._create_user, user_data)

    def save_admin(self, admin_data):
        with self.driver.session() as session:
            session.write_transaction(self._create_admin, admin_data)

    def get_user_recommendations(self, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._recommend_products, name)
            return result

    def get_admin_recommendations(self, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._recommend_reports, name)
            return result

    def populate_db(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_sample_data)

    @staticmethod
    def _create_user(tx, user_data):
        tx.run(
            """
            MERGE (u:User {name: $name})
            SET u.email = $email
            FOREACH (purchase IN $purchases | 
                MERGE (p:Purchase {id: purchase.id})
                SET p.item = purchase.item, p.price = purchase.price
                MERGE (u)-[:MADE]->(p))
            """,
            name=user_data["name"],
            email=user_data["email"],
            purchases=user_data["purchases"]
        )

    @staticmethod
    def _create_admin(tx, admin_data):
        tx.run(
            """
            MERGE (a:Admin {name: $name})
            SET a.email = $email
            FOREACH (report IN $reports |
                MERGE (r:Report {id: report.id})
                SET r.title = report.title, r.status = report.status
                MERGE (a)-[:CREATED]->(r))
            """,
            name=admin_data["name"],
            email=admin_data["email"],
            reports=admin_data["reports"]
        )

    @staticmethod
    def _create_sample_data(tx):
        tx.run(
            """
            MERGE (u:User {name: 'John Doe'})
            SET u.email = 'john@example.com'
            MERGE (p1:Purchase {id: 1, item: 'Laptop', price: 2500})
            MERGE (p2:Purchase {id: 2, item: 'Smartphone', price: 1200})
            MERGE (u)-[:MADE]->(p1)
            MERGE (u)-[:MADE]->(p2)

            MERGE (a:Admin {name: 'Admin Master'})
            SET a.email = 'admin@example.com'
            MERGE (r1:Report {id: 1, title: 'Monthly Sales', status: 'Completed'})
            MERGE (r2:Report {id: 2, title: 'User Activity', status: 'Pending'})
            MERGE (a)-[:CREATED]->(r1)
            MERGE (a)-[:CREATED]->(r2)
            """
        )

    @staticmethod
    def _recommend_products(tx, name):
        query = """
        MATCH (u:User {name: $name})-[:MADE]->(p:Purchase)
        WITH u, COLLECT(p.item) AS purchased_items
        MATCH (p:Purchase)
        WHERE NOT p.item IN purchased_items
        RETURN p.item AS recommended_item, COUNT(*) AS score
        ORDER BY score DESC
        LIMIT 5
        """
        result = tx.run(query, name=name)
        return [record["recommended_item"] for record in result]

    @staticmethod
    def _recommend_reports(tx, name):
        query = """
        MATCH (a:Admin {name: $name})-[:CREATED]->(r:Report)
        RETURN r.title AS report_title, r.status AS report_status
        ORDER BY r.status DESC
        LIMIT 5
        """
        result = tx.run(query, name=name)
        return [record["report_title"] for record in result]

# Modelos


class UserResponse(BaseModel):
    message: str
    data: dict


class AdminResponse(BaseModel):
    message: str
    data: dict


class RecommendationResponse(BaseModel):
    recommendations: List[str]

# Obter token de API fake


def get_fake_token(username: str, password: str):
    response = requests.post(
        f"{FAKE_API_URL}/token", params={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Unable to obtain token")

# Autenticação JWT


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Rotas da API


@app.get("/sync-user")
async def sync_user(username: str, password: str):
    token = get_fake_token(username, password)
    response = requests.get(f"{FAKE_API_URL}/user",
                            headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        user_data = response.json()["data"]
        client = Neo4jClient()
        client.save_user(user_data)
        client.close()
        return {"status": "success", "data": user_data}
    else:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)


@app.get("/sync-admin")
async def sync_admin(username: str, password: str):
    token = get_fake_token(username, password)
    response = requests.get(f"{FAKE_API_URL}/admin",
                            headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        admin_data = response.json()["data"]
        client = Neo4jClient()
        client.save_admin(admin_data)
        client.close()
        return {"status": "success", "data": admin_data}
    else:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)


@app.get("/user-recommendations")
async def user_recommendations(name: str):
    decoded_name = unquote(name)
    client = Neo4jClient()
    recommendations = client.get_user_recommendations(decoded_name)
    client.close()
    return {"recommendations": recommendations}


@app.get("/admin-recommendations")
async def admin_recommendations(name: str):
    decoded_name = unquote(name)
    client = Neo4jClient()
    recommendations = client.get_admin_recommendations(decoded_name)
    client.close()
    return {"recommendations": recommendations}


@app.get("/populate-db")
async def populate_db():
    client = Neo4jClient()
    client.populate_db()
    client.close()
    return {"status": "success", "message": "Database populated with sample data"}

# Função para criar um JWT


def create_jwt_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List
import requests
from neo4j import GraphDatabase
from jose import JWTError, jwt
from datetime import datetime, timedelta
from urllib.parse import quote, unquote
import os

# Carregar variáveis sensíveis de ambiente
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://a4051114.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "super-secure-password")
SECRET_KEY = os.getenv("SECRET_KEY", "your-very-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
FAKE_API_URL = os.getenv("FAKE_API_URL", "http://localhost:8000")

app = FastAPI()
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

    @staticmethod
    def _create_user(tx, user_data):
        tx.run("""
            MERGE (u:User {name: $name})
            SET u.email = $email
            FOREACH (purchase IN $purchases | 
                MERGE (p:Purchase {id: purchase.id})
                SET p.item = purchase.item, p.price = purchase.price
                MERGE (u)-[:MADE]->(p))
            """, name=user_data["name"], email=user_data["email"], purchases=user_data["purchases"])

    @staticmethod
    def _create_admin(tx, admin_data):
        tx.run("""
            MERGE (a:Admin {name: $name})
            SET a.email = $email
            FOREACH (report IN $reports |
                MERGE (r:Report {id: report.id})
                SET r.title = report.title, r.status = report.status
                MERGE (a)-[:CREATED]->(r))
            """, name=admin_data["name"], email=admin_data["email"], reports=admin_data["reports"])

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

# Modelos de dados


class UserData(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    purchases: List[dict]


class AdminData(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    reports: List[dict]


class RecommendationResponse(BaseModel):
    recommendations: List[str]

# Funções de autenticação e segurança


def create_jwt_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Funções da API


def get_fake_token(username: str, password: str):
    try:
        response = requests.post(
            f"{FAKE_API_URL}/token", params={"username": username, "password": password}, timeout=10)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503, detail=f"Error connecting to external service: {str(e)}")


@app.get("/sync-user")
async def sync_user(username: str, password: str):
    token = get_fake_token(username, password)
    response = requests.get(
        f"{FAKE_API_URL}/user", headers={"Authorization": f"Bearer {token}"}, timeout=10)
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
    response = requests.get(
        f"{FAKE_API_URL}/admin", headers={"Authorization": f"Bearer {token}"}, timeout=10)
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

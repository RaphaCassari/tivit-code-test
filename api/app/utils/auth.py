import requests
from fastapi import HTTPException
import os

FAKE_API_URL = os.getenv("FAKE_API_URL", "http://localhost:8000")

def get_fake_token(username: str, password: str):
    response = requests.post(f"{FAKE_API_URL}/token", params={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Unable to obtain token")

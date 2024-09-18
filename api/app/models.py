from pydantic import BaseModel
from typing import List

class UserResponse(BaseModel):
    message: str
    data: dict

class AdminResponse(BaseModel):
    message: str
    data: dict

class RecommendationResponse(BaseModel):
    recommendations: List[str]

class UserCredentials(BaseModel):
    username: str
    password: str

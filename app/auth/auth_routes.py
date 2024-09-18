from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user_schemas import Token, UserLogin

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("/token", response_model=Token)
def login_for_access_token(form_data: UserLogin):
    # Simulate a login process, should return a JWT token
    if form_data.username == "admin":
        return {"access_token": "fake-admin-jwt-token", "token_type": "bearer"}
    return {"access_token": "fake-user-jwt-token", "token_type": "bearer"}

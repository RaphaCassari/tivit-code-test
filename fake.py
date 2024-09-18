from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Configurações do JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Simulação de um banco de dados de usuários
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "adminpass",  # Senha não criptografada
        "role": "admin",
        "name": "Admin Master",
        "email": "admin@example.com",
        "reports": [
            {"id": 1, "title": "Monthly Sales", "status": "Completed"},
            {"id": 2, "title": "User Activity", "status": "Pending"}
        ]
    },
    "user": {
        "username": "user",
        "password": "userpass",  # Senha não criptografada
        "role": "user",
        "name": "John Doe",
        "email": "john@example.com",
        "purchases": [
            {"id": 1, "item": "Laptop", "price": 2500},
            {"id": 2, "item": "Smartphone", "price": 1200}
        ]
    }
}

# Models


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    role: str = None


class Purchase(BaseModel):
    id: int
    item: str
    price: float


class UserData(BaseModel):
    name: str
    email: str
    purchases: List[Purchase]


class UserResponse(BaseModel):
    message: str
    data: UserData


class Report(BaseModel):
    id: int
    title: str
    status: str


class AdminData(BaseModel):
    name: str
    email: str
    reports: List[Report]


class AdminResponse(BaseModel):
    message: str
    data: AdminData


# Dependência de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username, role=role)
        return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# POST /token: Login and return a token based on user role


@app.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Criar payload diferente para user e admin
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username, "role": user["role"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependência para pegar o usuário atual a partir do token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = verify_access_token(token)
    user = fake_users_db.get(token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# GET /user: Return user data


@app.get("/user", response_model=UserResponse)
async def read_user_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Resposta com a mensagem e dados do usuário
    response = {
        "message": "Hello, user!",
        "data": {
            "name": current_user["name"],
            "email": current_user["email"],
            "purchases": current_user["purchases"]
        }
    }
    return response

# GET /admin: Return admin data if the user is an admin


@app.get("/admin", response_model=AdminResponse)
async def read_admin_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Resposta com a mensagem e dados do admin
    response = {
        "message": "Hello, admin!",
        "data": {
            "name": current_user["name"],
            "email": current_user["email"],
            "reports": current_user["reports"]
        }
    }
    return response

# GET /health: Health check


@app.get("/health")
async def health_check():
    return {"status": "ok"}

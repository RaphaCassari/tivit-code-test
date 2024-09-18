from fastapi import FastAPI
from app.auth.auth_routes import auth_router
from app.routes.sync_routes import sync_router
from app.routes.recommendation_routes import recommendation_router
from fastapi.middleware.cors import CORSMiddleware

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


# Include routes
app.include_router(auth_router)
app.include_router(sync_router)
app.include_router(recommendation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)

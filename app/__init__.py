from fastapi import FastAPI
from app.routes.sync_routes import sync_router
from app.routes.recommendation_routes import recommendation_router
from app.auth.auth_routes import auth_router

app = FastAPI()

# Include routes
app.include_router(sync_router)
app.include_router(recommendation_router)
app.include_router(auth_router)

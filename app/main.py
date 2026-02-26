from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.api import auth, user, queries
from app.core.config import settings
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MediAssist Pro API", 
    version="1.0.0",
    description="Assistant Cognitif de Maintenance Biomédicale"
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(queries.router)

@app.get("/")
def root():
    return {
        "message": "MediAssist Pro API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/test")
def test_endpoint():
    return {"message": "Backend is working!", "timestamp": "2026-02-04"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
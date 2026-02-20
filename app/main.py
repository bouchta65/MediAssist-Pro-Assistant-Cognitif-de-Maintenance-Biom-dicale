from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api import auth, user, queries
from app.core.config import settings
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

class NgrokCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            response = Response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response
        
        # Handle actual requests
        try:
            response = await call_next(request)
        except Exception as e:
            # Create error response with CORS headers
            response = Response(content=str(e), status_code=500)
        
        # Always add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

app = FastAPI(
    title="MediAssist Pro API", 
    version="1.0.0",
    description="Assistant Cognitif de Maintenance Biomédicale"
)

# Add custom CORS middleware for ngrok
app.add_middleware(NgrokCORSMiddleware)

# Add session middleware for OAuth
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(queries.router)

@app.options("/{path:path}")
async def options_handler(path: str):
    return {"message": "OK"}

@app.get("/")
async def root():
    return {
        "message": "MediAssist Pro API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/test")
async def test_endpoint():
    return {"message": "Backend is working!", "timestamp": "2026-02-04"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
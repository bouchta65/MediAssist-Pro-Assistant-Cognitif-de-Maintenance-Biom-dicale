from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.oauth import google, get_google_user_info
from app.schemas.user_schema import Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    try:
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        response = await google.authorize_redirect(request, redirect_uri)
        return response
    except Exception as e:
        print(f"Error in google_login: {e}")
        raise

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback"""
    try:        
        token = await google.authorize_access_token(request)
        
        user_info = await get_google_user_info(request, token)
        
        # Check if user exists by Google ID
        user = UserService.get_user_by_google_id(db, user_info['google_id'])
        
        if not user:
            # Check if user exists by email
            user = UserService.get_user_by_email(db, user_info['email'])
            if user:
                # Link Google account to existing user
                user = UserService.link_google_account(db, user, user_info['google_id'])
            else:
                # Create new user
                user = UserService.create_oauth_user(db, user_info)
        
        access_token = AuthService.create_access_token(data={"sub": user.email})
        
        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?token={access_token}",
            status_code=302
        )
        
    except Exception as e:
        return RedirectResponse(
            url="http://localhost:3000/auth/error",
            status_code=302
        )

@router.post("/register")
async def register(email: str = Form(...), password: str = Form(...), username: str = Form(...), db: Session = Depends(get_db)):
    """Register new user"""
    if UserService.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = {
        'username': username,
        'email': email,
        'hashed_password': UserService.hash_password(password),
        'is_oauth': False
    }
    user = UserService.create_user(db, user_data)
    
    return {
        "message": "Registration successful! Please login with your credentials.",
        "redirect": "/login",
        "user": {
            "email": user.email,
            "username": user.username
        }
    }

@router.post("/login", response_model=Token)
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Regular email/password login"""
    user = UserService.get_user_by_email(db, email)
    if not user or not UserService.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = AuthService.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
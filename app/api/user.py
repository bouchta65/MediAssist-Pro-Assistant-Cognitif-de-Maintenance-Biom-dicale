from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserResponse, UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db)):
    pass

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = user.dict()
    if user_data.get('password'):
        user_data['hashed_password'] = UserService.hash_password(user_data.pop('password'))
    
    return UserService.create_user(db, user_data)
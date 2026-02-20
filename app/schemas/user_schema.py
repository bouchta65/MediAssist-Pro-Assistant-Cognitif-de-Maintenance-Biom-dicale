from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional



class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: Optional[str] = None  # Optional for OAuth users
    google_id: Optional[str] = None
    is_oauth: bool = False


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: str
    is_oauth: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: int
    role: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)



class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None
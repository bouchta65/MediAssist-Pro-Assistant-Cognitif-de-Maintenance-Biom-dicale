from sqlalchemy.orm import Session
import bcrypt
from app.models.users import Users

class UserService:
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(Users).filter(Users.email == email).first()
    
    @staticmethod
    def get_user_by_google_id(db: Session, google_id: str):
        return db.query(Users).filter(Users.google_id == google_id).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(Users).filter(Users.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user_data: dict):
        db_user = Users(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def create_oauth_user(db: Session, user_info: dict):
        user_data = {
            'username': user_info['username'],
            'email': user_info['email'],
            'google_id': user_info['google_id'],
            'is_oauth': True,
            'hashed_password': None
        }
        return UserService.create_user(db, user_data)
    
    @staticmethod
    def link_google_account(db: Session, user: Users, google_id: str):
        user.google_id = google_id
        user.is_oauth = True
        db.commit()
        return user
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        if hashed_password is None:
            return False
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def hash_password(password: str):
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
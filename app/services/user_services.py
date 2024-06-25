from app.models.user import UserCreate, UserLogin
from app.models.models import SessionLocal,get_db
from app.models import models

def create_user(user: UserCreate):
    with get_db() as db:
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

def get_user(email: str):
     with get_db() as db:
        user = db.query(models.User).filter(models.User.email == email).first() 
        return user

def get_user_by_id(id: str):
    with get_db() as db:
        user = db.query(models.User).filter(models.User.id == id).first()
        return user

def get_users_from_db():
    with get_db() as db:
        users = db.query(UserCreate).all()
        return users
    
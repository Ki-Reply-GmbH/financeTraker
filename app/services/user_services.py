from app.models.user import UserCreate, UserLogin
from app.models.models import SessionLocal
from app.models import models

def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

def get_user(email: str):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()    
    db.close()
    return user

def get_users_from_db():
    db = SessionLocal()
    users = db.query(UserCreate).all()
    db.close()
    return users
    
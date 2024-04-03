from fastapi import APIRouter
from app.models.user import UserCreate, UserLogin
from app.services.user_services import create_user,get_users_from_db,get_user

router = APIRouter()

@router.get("/user/getUsers")
async def get_users():
    users=get_users_from_db()
    return {"users": users}

@router.post("/user/register")
async def register_user(user: UserCreate):
    create_user(user)
    return {"message": "User registered successfully"}

@router.post("/user/login")
async def login(user: UserLogin):
    user=get_user(user.email)
    return {"message": "User logged in successfully"}

@router.post("/user/logout")
async def logout():
    # Logout logic here
    return {"message": "User logged out successfully"}
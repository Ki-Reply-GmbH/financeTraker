from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from app.models.user import UserCreate, UserLogin
from app.services.auth import create_access_token, get_current_user
from app.services.user_services import create_user,get_users_from_db,get_user
from app import get_logger


logger = get_logger(__name__)

router = APIRouter()

@router.get("/user/getUsers")
async def get_users():
    users=get_users_from_db()
    return {"users": users}

@router.post("/user/register")
async def register_user(user: UserCreate):
    try:
        create_user(user)
        return {"message": "User registered successfully"}
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return {"message": "Error registering user"}

@router.post("/user/login")
async def login(user: UserLogin):
    user=get_user(user.email)
    access_token = create_access_token(data={"sub": user.id})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

@router.post("/user/logout")
async def logout():
    # Logout logic here
    return {"message": "User logged out successfully"}

@router.get("/user/authTest")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    logger.info(f"testing authentication")
    logger.info(f"current_user: {current_user}")
    return current_user
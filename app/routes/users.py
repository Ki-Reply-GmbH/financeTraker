from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from models.user import UserCreate, UserLogin
from services.auth import create_access_token, get_current_user
from services.user_services import create_user,get_user
from logger import get_logger
from fastapi import HTTPException


logger = get_logger(__name__)

router = APIRouter()

@router.post("/user/register")
async def register_user(user: UserCreate):
    try:
        create_user(user)
        return {"message": "User registered successfully"}
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error registering user")

@router.post("/user/login")
async def login(user: UserLogin):
    try:
        user = get_user(user.email)
        if user is None:
            return {"message": "User not found"}
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        return {"message": "Error retrieving user"}
    access_token = create_access_token(data={"sub": user.id})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

@router.post("/user/logout")
async def logout():
    # Logout logic here
    return {"message": "User logged out successfully"}

@router.get("/user/authTest")
async def read_users_me(current_user: dict = Depends(get_current_user)):
logger.info("testing authentication")
    logger.info(f"current_user: {current_user}")
    return current_user
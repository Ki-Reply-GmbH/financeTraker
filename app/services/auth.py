import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from app.config import get_secret_key,get_access_token_expire_minutes
from app.services.user_services import get_user_by_id
from app.logger import get_logger
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logger = get_logger(__name__)

SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_access_token_expire_minutes()) or 30

def create_access_token(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.info(f"SECRET_KEY: {SECRET_KEY}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user=get_user_by_id(user_id)
        return {"user": user, "token": token}
    except PyJWTError:  # Use PyJWTError instead of JWTError
        raise credentials_exception




# # auth.py
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi_login import LoginManager
# from fastapi_login.exceptions import InvalidCredentialsException
# from passlib.context import CryptContext
# from app.services.user_services import get_user 

# SECRET = "secret-key"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# manager = LoginManager(SECRET, tokenUrl='/auth/token', use_cookie=True)

# @manager.user_loader
# def load_user(email: str): 
#     return User.get(email)  # adjust this according to your User model

# def login(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password

#     user = User.get(email)  # adjust this according to your User model
#     if not user or not pwd_context.verify(password, user.password):
#         raise InvalidCredentialsException

#     access_token = manager.create_access_token(
#         data=dict(sub=email)
#     )
#     return {'access_token': access_token, 'token_type': 'bearer'}
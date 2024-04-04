from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: str
    password: str
    
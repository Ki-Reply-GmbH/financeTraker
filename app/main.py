from fastapi import FastAPI
from routes.users import router as UserRouter

app = FastAPI()

app.include_router(UserRouter)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

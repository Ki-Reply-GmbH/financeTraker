from fastapi import FastAPI
from .routes.users import router as UserRouter
from .config import DATABASE_URL, test_connection

app = FastAPI()

async def startup_event():
    await test_connection()

app.add_event_handler("startup", startup_event)

app.include_router(UserRouter)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


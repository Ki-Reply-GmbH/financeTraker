from fastapi import FastAPI
from .routes.users import router as UserRouter
from .config import DATABASE_URL, test_connection

app = FastAPI()

async def test_database_connection_on_startup():
    await test_connection()

app.include_router(UserRouter)

app.add_event_handler("startup", test_database_connection_on_startup)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


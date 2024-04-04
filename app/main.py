from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routes.users import router as UserRouter
from app.config import DATABASE_URL, test_connection
from app.models.models import Base, engine  # Import Base and engine from your models module

app = FastAPI()

async def test_database_connection_on_startup():
    await test_connection()

    # Create the database tables
    Base.metadata.create_all(bind=engine)

app.include_router(UserRouter)

app.add_event_handler("startup", test_database_connection_on_startup)

@app.get("/", response_class=FileResponse)
async def read_home():
    return "./app/static/UI/user.html"
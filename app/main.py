from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routes.users import router as UserRouter
from app.config import DATABASE_URL, test_connection
from app.models.models import Base, engine  # Import Base and engine from your models module

app = FastAPI()

async def startup_event():
    await test_connection()

    # Create the database tables
    Base.metadata.create_all(bind=engine)

app.add_event_handler("startup", startup_event)

app.include_router(UserRouter)

@app.get("/", response_class=FileResponse)
async def read_home():
    return "./app/static/UI/user.html"
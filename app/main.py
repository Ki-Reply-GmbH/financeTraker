
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from routes.users import router as UserRouter
from routes.transactions import router as TransactionRouter
from config import DATABASE_URL, test_connection, secret_generator
from models.models import Base, engine
from logger import get_logger
import os

logger = get_logger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

async def test_database_connection_on_startup():
    await test_connection()
    Base.metadata.create_all(bind=engine)

app.include_router(UserRouter)
app.include_router(TransactionRouter)
app.add_event_handler("startup", test_database_connection_on_startup)

if not os.getenv("SECRET_KEY"):
    logger.info("Generating new secret key")
    secret=secret_generator()
    with open('.env', 'a') as f:
        f.write(f'\nSECRET_KEY={secret}\n')
    
@app.get("/", response_class=HTMLResponse)
async def read_home():
    return FileResponse("./app/static/UI/dashboard.html")

@app.get("/ui/{id}", response_class=HTMLResponse)
async def read_ui(id: str):
    return FileResponse(path=f"./app/static/UI/{id}.html", headers={"Content-Disposition": "inline; filename='{id}.html'"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

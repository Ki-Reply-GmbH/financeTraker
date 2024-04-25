from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from routes.users import router as UserRouter
from routes.transactions import router as TransactionRouter
from config import DATABASE_URL, test_connection, secret_generator
from models.models import Base, engine
from logger import get_logger
import os
import re

logger = get_logger(__name__)

app = FastAPI()

async def test_database_connection_on_startup():
    await test_connection()
    Base.metadata.create_all(bind=engine)

app.include_router(UserRouter)
app.include_router(TransactionRouter)

app.add_event_handler("startup", test_database_connection_on_startup)

if not os.getenv("SECRET_KEY"):
    logger.info("Generating new secret key")
    secret = secret_generator()
    with open('.env', 'a') as f:
        f.write(f'\nSECRET_KEY={secret}\n')

@app.get("/", response_class=HTMLResponse)
async def read_home():
    path = os.path.abspath("./app/static/UI/dashboard.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Page not found")
    with open(path) as f:
        html_content = f.read()
    return html_content

@app.get("/ui/{id}", response_class=HTMLResponse)
async def read_ui(id: str):
    if not re.match(r'^[a-zA-Z0-9_\-]+$', id):
        raise HTTPException(status_code=400, detail="Invalid file request")
    path = os.path.abspath(f"./app/static/UI/{id}.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Page not found")
    with open(path) as f:
        html_content = f.read()
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
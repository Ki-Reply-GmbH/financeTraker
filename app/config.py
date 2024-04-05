
from dotenv import load_dotenv
import os
from databases import Database
from app import get_logger

logger = get_logger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables")


database = Database(DATABASE_URL)

async def test_connection():
    try:
        await database.connect()
        logger.info("Connected to the database!")
        await database.disconnect()
        logger.info("Disconnected from the database!")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")

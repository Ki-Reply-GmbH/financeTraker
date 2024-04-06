
from dotenv import load_dotenv
import os
from databases import Database
from app import get_logger
import secrets

logger = get_logger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_Key = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables")


database = Database(DATABASE_URL)

async def test_connection():

        try:
            await database.connect()
            logger.info("Connected to the database!")
            # Your code here
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
        finally:
            await database.disconnect()
            logger.info("Disconnected from the database!")
            
def secret_generator():
    return secrets.token_hex(32)

def get_secret_key():
    return SECRET_Key

def get_access_token_expire_minutes():
    return ACCESS_TOKEN_EXPIRE_MINUTES

            

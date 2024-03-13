
from dotenv import load_dotenv
import os
from databases import Database


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


database = Database(DATABASE_URL)

async def test_connection():
    await database.connect()
    print("Connected to the database!")
    await database.disconnect()
    print("Disconnected from the database!")


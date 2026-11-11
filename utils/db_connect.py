
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing in .env file")

    connection = psycopg2.connect(DATABASE_URL)

    return connection

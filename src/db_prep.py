import os
from dotenv import load_dotenv

os.environ['RUN_TIMEZONE_CHECK'] = '0'

from db import init_db

load_dotenv()
os.environ['POSTGRES_HOST'] = 'localhost'

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized.")
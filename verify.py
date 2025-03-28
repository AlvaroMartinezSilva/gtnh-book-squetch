# 🔁 This file should be split into modules under models/
# The following is a fallback check script to verify model loading and DB creation

import os
from sqlalchemy import create_engine
from models import Base, User, Library, Permission, Shelf, Collection, Book, Page
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "sqlite:///gtnh_library.db")
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    try:
        Base.metadata.create_all(engine)
        print("✅ All models loaded and database schema created successfully.")
    except Exception as e:
        print("❌ Error creating database schema:", e)
        raise

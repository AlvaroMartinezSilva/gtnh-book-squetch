import os
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "sqlite:///gtnh_library.db")

engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Database created successfully.")

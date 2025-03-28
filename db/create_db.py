import os
from sqlalchemy import create_engine
from models import Base  # Asegúrate de tener un __init__.py en models
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Usa PostgreSQL por defecto si está definido
DATABASE_URL = os.getenv("DB_URL", "sqlite:///gtnh_library.db")
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("📚 Database created successfully.")

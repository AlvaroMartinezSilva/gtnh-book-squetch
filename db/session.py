from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.getenv("DB_URL", "sqlite:///gtnh_library.db"))

SessionLocal = sessionmaker(bind=engine)

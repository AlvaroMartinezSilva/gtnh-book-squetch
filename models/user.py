import hashlib
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    libraries = relationship("Library", back_populates="owner")
    permissions = relationship("Permission", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

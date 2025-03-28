import hashlib
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Library(Base):
    __tablename__ = 'libraries'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String)
    password_hash = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="libraries")
    shelves = relationship("Shelf", back_populates="library")
    permissions = relationship("Permission", back_populates="library")

    def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return True
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password: str):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

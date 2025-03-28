from sqlalchemy import Column, Integer, ForeignKey, Boolean ,String
from sqlalchemy.orm import relationship
from models import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    tags = Column(String, nullable=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))
    collection = relationship("Collection", back_populates="books")
    pages = relationship("Page", back_populates="book")
from sqlalchemy import Column, Integer, ForeignKey, Boolean , String
from sqlalchemy.orm import relationship
from models import Base


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    shelf_id = Column(Integer, ForeignKey('shelves.id'))
    shelf = relationship("Shelf", back_populates="collections")
    books = relationship("Book", back_populates="collection")
from sqlalchemy import Column, Integer, ForeignKey, Boolean , String
from sqlalchemy.orm import relationship
from models import Base


class Shelf(Base):
    __tablename__ = 'shelves'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    library_id = Column(Integer, ForeignKey('libraries.id'))
    library = relationship("Library", back_populates="shelves")
    collections = relationship("Collection", back_populates="shelf")
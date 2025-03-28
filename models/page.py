from sqlalchemy import Column, Integer, ForeignKey, Boolean ,String,Text,DateTime
from sqlalchemy.orm import relationship
from models import Base

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    title = Column(String)
    page_type = Column(String)
    content = Column(Text)
    images = Column(Text)
    canvas_data = Column(Text)  # Stores JSON from drawable canvas
    created_at = Column(DateTime)
    book = relationship("Book", back_populates="pages")
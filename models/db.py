import hashlib
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Boolean, create_engine
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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

class Library(Base):
    __tablename__ = 'libraries'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)

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

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    library_id = Column(Integer, ForeignKey('libraries.id'))

    can_view = Column(Boolean, default=True)
    can_edit = Column(Boolean, default=False)

    user = relationship("User", back_populates="permissions")
    library = relationship("Library", back_populates="permissions")

class Shelf(Base):
    __tablename__ = 'shelves'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    library_id = Column(Integer, ForeignKey('libraries.id'))

    library = relationship("Library", back_populates="shelves")
    collections = relationship("Collection", back_populates="shelf")

class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    shelf_id = Column(Integer, ForeignKey('shelves.id'))

    shelf = relationship("Shelf", back_populates="collections")
    books = relationship("Book", back_populates="collection")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    tags = Column(String, nullable=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))

    collection = relationship("Collection", back_populates="books")
    pages = relationship("Page", back_populates="book")

class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))

    title = Column(String)
    page_type = Column(String)
    content = Column(Text)
    images = Column(Text)
    canvas_data = Column(Text)
    created_at = Column(DateTime)

    book = relationship("Book", back_populates="pages")
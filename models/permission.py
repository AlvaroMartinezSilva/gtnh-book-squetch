from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    library_id = Column(Integer, ForeignKey('libraries.id'))
    can_view = Column(Boolean, default=True)
    can_edit = Column(Boolean, default=False)
    user = relationship("User", back_populates="permissions")
    library = relationship("Library", back_populates="permissions")

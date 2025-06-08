from .database import Base
from sqlalchemy.sql import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False) 
    title = Column(String, nullable=False) 
    content = Column(String, nullable=False) 
    published = Column(Boolean,default=True, nullable=False) 
    created_at=Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False) 
    owner_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
from .database import Base

from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=True)

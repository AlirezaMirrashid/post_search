
import uuid, time
from sqlalchemy import Column, String, Integer, Text, Float
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    created_at = Column(Float, default=time.time)
    like_count = Column(Integer, default=0)
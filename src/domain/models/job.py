from sqlalchemy import Column, Integer, String, Text
from src.domain.db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    intent_hash = Column(String(64), index=True)
    task = Column(Text)
    status = Column(String(32))

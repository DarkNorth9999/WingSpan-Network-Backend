from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Airport(Base):
    __tablename__ = "airports"

    code = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

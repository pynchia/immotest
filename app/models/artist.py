from sqlalchemy import Boolean, Column, Integer, String

from app.db import Base


class Artist(Base):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    popularity = Column(Integer, nullable=False)
    updated_by_be = Column(Boolean, default=False, nullable=False)

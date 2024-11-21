from sqlalchemy import Column, Integer, String
from app.database.data import Base


class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)

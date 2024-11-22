from sqlalchemy import Column, Integer, String
from app.database.data import Base

class Competicao(Base):
    __tablename__ = "competicoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    modalidade = Column(String, nullable=False)
    ano_competicao = Column(Integer, nullable=False)

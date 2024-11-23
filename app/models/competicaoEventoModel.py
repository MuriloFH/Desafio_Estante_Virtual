from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.data import Base
from sqlalchemy.orm import relationship
from app.models.competicaoModel import Competicao
from app.models.competidorModel import Competitor

class CompeticaoEvento(Base):
    __tablename__ = "competicoes_eventos"

    id = Column(Integer, primary_key=True, index=True)
    competicao_id = Column(Integer, ForeignKey("competicoes.id"), nullable=False)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False)
    value = Column(String, nullable=False)
    unidade = Column(String, nullable=False)

    competicao = relationship("Competicao", back_populates="eventos")
    competitor = relationship("Competitor", back_populates="eventos")


Competicao.eventos = relationship("CompeticaoEvento", back_populates="competicao")
Competitor.eventos = relationship("CompeticaoEvento", back_populates="competitor")
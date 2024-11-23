from pydantic import BaseModel
from app.schemas.competidorSchema import CompetitorResponse
from app.schemas.competicaoSchema import CompeticaoResponse

class CompeticaoEventoBase(BaseModel):
    competicao_id: int
    competitor_id: int
    value: str
    unidade: str
    
class CompeticaoEventoResponse(BaseModel):
    id: int
    competitor: CompetitorResponse
    competicao: CompeticaoResponse
    value: str
    unidade: str

class CompeticaoEventoCreate(CompeticaoEventoBase):
    pass

class CompeticaoEvento(CompeticaoEventoBase):
    id: int

    class Config:
        orm_mode = True

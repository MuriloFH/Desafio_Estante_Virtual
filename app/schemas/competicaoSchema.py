from pydantic import BaseModel

class CompeticaoBase(BaseModel):
    descricao: str
    modalidade: str
    ano_competicao: int
    status: str

class CompeticaoResponse(BaseModel):
    id: int
    descricao: str
    modalidade: str

class CompeticaoCreate(CompeticaoBase):
    pass

class Competicao(CompeticaoBase):
    id: int

    class Config:
        orm_mode = True

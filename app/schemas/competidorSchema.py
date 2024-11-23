from pydantic import BaseModel

class CompetitorBase(BaseModel):
    identifier: str
    name: str
    cpf: str

class CompetitorResponse(BaseModel):
    id: int
    competitor_name: str
    
class CompetitorCreate(CompetitorBase):
    pass

class Competitor(CompetitorBase):
    id: int

    class Config:
        orm_mode = True

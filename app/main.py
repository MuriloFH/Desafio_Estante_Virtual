from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.data import Base, engine, SessionLocal
# ------------------------ competidores ------------------------
from app.schemas.competidorSchema import CompetitorCreate, Competitor
from app.crud.competidorCrud import (
    create_competitor,
    get_competitors,
    get_competitor,
    delete_competitor,
    update_competitor,
)
# ------------------------ competicao ------------------------
from app.schemas.competicaoSchema import Competicao, CompeticaoCreate
from app.crud.competicaoCrud import (
    create_competicao,
    get_competicao,
    get_competicoes,
    delete_competicao,
    update_competicao
)

# Inicializa as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/competitors/", response_model=Competitor)
def create_competitor_endpoint(competitor: CompetitorCreate, db: Session = Depends(get_db)):
    return create_competitor(db=db, competitor=competitor)

@app.get("/competitors/", response_model=list[Competitor])
def read_competitors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_competitors(db=db, skip=skip, limit=limit)

@app.get("/competitors/{competitor_id}", response_model=Competitor)
def read_competitor(competitor_id: int, db: Session = Depends(get_db)):
    competitor = get_competitor(db=db, competitor_id=competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor

@app.delete("/competitors/{competitor_id}")
def delete_competitor_endpoint(competitor_id: int, db: Session = Depends(get_db)):
    deleted_competitor = delete_competitor(db=db, competitor_id=competitor_id)
    if not deleted_competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return {"detail": "Competitor deleted"}

@app.put("/competitors/{competitor_id}", response_model=Competitor)
def update_competitor_endpoint(
    competitor_id: int, competitor: CompetitorCreate, db: Session = Depends(get_db)
):
    updated_competitor = update_competitor(
        db=db, competitor_id=competitor_id, updated_data=competitor
    )
    if not updated_competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return updated_competitor


@app.post("/competicao/", response_model=Competicao)
def create_competicao_endpoint(competicao: CompeticaoCreate, db: Session = Depends(get_db)):
    return create_competicao(db=db, competicao=competicao)


@app.get("/competicao/", response_model=list[Competicao])
def read_competicao(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_competicoes(db=db, skip=skip, limit=limit)


@app.get("/competicao/{competicao_id}", response_model=Competicao)
def read_competicao(competicao_id: int, db: Session = Depends(get_db)):
    competicao = get_competicao(db=db, competicao_id=competicao_id)

    return competicao if competicao else HTTPException(status_code=404, detail="Competição não localizada.")


@app.delete("/competicao/{competicao_id}")
def delete_competicao_endpoint(competicao_id: int, db: Session = Depends(get_db)):
    deleted_competicao = delete_competicao(db=db, competicao_id=competicao_id)
    
    return deleted_competicao if deleted_competicao else HTTPException(status_code=404, detail="Competição não localizada.")


@app.put("/competicao/{competicao_id}", response_model=Competicao)
def update_competicao_endpoint(
    competicao_id: int, competicao: CompeticaoCreate, db: Session = Depends(get_db)
):
    updated_competicao= update_competicao(
        db=db, competicao_id=competicao_id, update_data=competicao
    )
    
    return updated_competicao if updated_competicao else HTTPException(status_code=404, detail="Competição não localizada.")

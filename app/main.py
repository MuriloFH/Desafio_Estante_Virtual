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
# ------------------------ competicao evento ------------------------
from app.schemas.competicaoEventoSchema import CompeticaoEvento, CompeticaoEventoResponse, CompeticaoEventoCreate
from app.crud.competicaoEventoCrud import (
    create_competicao_evento,
    get_competicao_evento_response,
    get_competicao_evento,
    get_competicoes_eventos,
    delete_competicao_evento,
    update_competicao_evento
)
# ------------------------ competicao evento Ranking ------------------------
from app.crud.competicaoEventoRankingCrud import get_competicao_evento_ranking_response

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

# -------------- Competição --------------

@app.post("/competicao/", response_model=Competicao)
def create_competicao_endpoint(competicao: CompeticaoCreate, db: Session = Depends(get_db)):
    return create_competicao(db=db, competicao=competicao)


@app.get("/competicao/", response_model=list[Competicao])
def read_competicao(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_competicoes(db=db, skip=skip, limit=limit)


@app.get("/competicao/{competicao_id}", response_model=Competicao)
def read_competicao(competicao_id: int, db: Session = Depends(get_db)):
    competicao = get_competicao(db=db, competicao_id=competicao_id)

    if competicao:
        return competicao

    raise HTTPException(status_code=404, detail="Competição não localizada.")


@app.delete("/competicao/{competicao_id}")
def delete_competicao_endpoint(competicao_id: int, db: Session = Depends(get_db)):
    deleted_competicao = delete_competicao(db=db, competicao_id=competicao_id)
    
    if deleted_competicao:
        return {"detail": "Competição deletada com sucesso!"}

    raise HTTPException(status_code=404, detail="Competição não localizada.")


@app.put("/competicao/{competicao_id}", response_model=Competicao)
def update_competicao_endpoint(
    competicao_id: int, competicao: CompeticaoCreate, db: Session = Depends(get_db)
):
    updated_competicao= update_competicao(
        db=db, competicao_id=competicao_id, update_data=competicao
    )
    
    if updated_competicao:
        return updated_competicao

    raise HTTPException(status_code=404, detail="Competição não localizada.")



# -------------- Competição Evento --------------

@app.post("/competicao-evento/", response_model=CompeticaoEvento)
def create_competicao_evento_endpoint(competicao: CompeticaoEventoCreate, db: Session = Depends(get_db)):
    return create_competicao_evento(db=db, competicao=competicao)


@app.get("/competicao-evento/", response_model=list[CompeticaoEventoResponse])
def read_competicao_evento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_competicoes_eventos(db=db, skip=skip, limit=limit)


@app.get("/competicao-evento/{competicao_evento_id}", response_model=CompeticaoEventoResponse)
def read_competicao_evento(competicao_evento_id:int, db: Session = Depends(get_db)):
    competicao_evento = get_competicao_evento_response(db=db, competicao_id=competicao_evento_id)
    
    if competicao_evento:
        return competicao_evento

    raise HTTPException(status_code=404, detail="Evento da competição não localizado.")


@app.delete("/competicao-evento/{competicao_evento_id}")
def delete_competicao_evento_endpoint(competicao_evento_id: int, db: Session = Depends(get_db)):
    deleted_competicao_evento = delete_competicao_evento(db=db, competicao_id=competicao_evento_id)
    
    if deleted_competicao_evento:
        return {"detail": "Evento da competição deletado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Evento da competição não localizado.")


@app.put("/competicao-evento/{competicao_evento_id}", response_model=CompeticaoEvento)
def update_competicao_endpoint(competicao_evento_id: int, competicao: CompeticaoEventoCreate, db: Session = Depends(get_db)):
    updated_competicao_evento= update_competicao_evento(db=db, competicao_id=competicao_evento_id, update_data=competicao)
    
    if updated_competicao_evento:
        return updated_competicao_evento
    else:
        raise HTTPException(status_code=404, detail="Evento da competição não localizado.")


# -------------- Competição Ranking --------------
@app.get("/competicao/{competicao_id}/ranking", response_model=dict)
def get_competicao_evento_ranking_endpoint(competicao_id: int, db: Session = Depends(get_db)):
    return get_competicao_evento_ranking_response(db=db, competicao_id=competicao_id)
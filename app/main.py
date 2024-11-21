from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.data import Base, engine, SessionLocal
from app.schemas.competidorSchema import CompetitorCreate, Competitor
from app.crud.competidorCrud import (
    create_competitor,
    get_competitors,
    get_competitor,
    delete_competitor,
    update_competitor,
)
from app.models.competidorModel import Competitor as CompetitorModel

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
def read_competitors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
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

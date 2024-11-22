from sqlalchemy.orm import Session
from app.models.competidorModel import Competitor
from app.schemas.competidorSchema import CompetitorCreate

def get_competitor(db: Session, competitor_id: int):
    return db.query(Competitor).filter(Competitor.id == competitor_id).first()

def get_competitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competitor).offset(skip).limit(limit).all()

def create_competitor(db: Session, competitor: CompetitorCreate):
    db_competitor = Competitor(
        identifier=competitor.identifier, name=competitor.name, cpf=competitor.cpf
    )
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    return db_competitor

def delete_competitor(db: Session, competitor_id: int):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if competitor:
        db.delete(competitor)
        db.commit()
    return competitor

def update_competitor(db: Session, competitor_id: int, updated_data: CompetitorCreate):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if competitor:
        competitor.identifier = updated_data.identifier
        competitor.name = updated_data.name
        competitor.cpf = updated_data.cpf
        db.commit()
        db.refresh(competitor)
    return competitor

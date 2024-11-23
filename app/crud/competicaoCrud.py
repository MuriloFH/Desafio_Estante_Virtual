from sqlalchemy.orm import Session
from app.models.competicaoModel import Competicao
from app.schemas.competicaoSchema import CompeticaoCreate

def get_competicao(db: Session, competicao_id: int):
    return db.query(Competicao).filter(Competicao.id == competicao_id).first()


def get_competicoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competicao).offset(skip).limit(limit).all()


def create_competicao(db: Session, competicao: CompeticaoCreate):
    newCompeticao = Competicao(descricao=competicao.descricao,
                               modalidade=competicao.modalidade,
                               ano_competicao=competicao.ano_competicao,
                               status=competicao.status)
    
    db.add(newCompeticao)
    db.commit()
    db.refresh(newCompeticao)
    return newCompeticao

def delete_competicao(db: Session, competicao_id: int):
    competicao_delete = get_competicao(db, competicao_id)
    
    if competicao_delete:
        db.delete(competicao_delete)
        db.commit()
        
    return competicao_delete


def update_competicao(db: Session, competicao_id: int, update_data: CompeticaoCreate):
    competicao_update = get_competicao(db, competicao_id)

    if competicao_update:
        competicao_update.descricao = update_data.descricao
        competicao_update.modalidade = update_data.modalidade
        competicao_update.ano_competicao = update_data.ano_competicao
        competicao_update.status = update_data.status
        
        db.commit()
        db.refresh(competicao_update)
    return competicao_update
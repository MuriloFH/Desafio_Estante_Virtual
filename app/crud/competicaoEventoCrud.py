from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.competicaoEventoModel import CompeticaoEvento
from app.schemas.competicaoEventoSchema import CompeticaoEventoCreate
from app.models.competidorModel import Competitor
from app.models.competicaoModel import Competicao

def get_competicao_evento_response(db: Session, competicao_id: int):
    
    query = (
        db.query(
            CompeticaoEvento.id,
            CompeticaoEvento.value,
            CompeticaoEvento.unidade,
            Competitor.id.label("competitor_id"),
            Competitor.name.label("competitor_name"),
            Competicao.id.label("competicao_id"),
            Competicao.descricao.label("competicao_descricao"),
            Competicao.modalidade.label("competicao_modalidade"),
        )
        .join(Competitor, CompeticaoEvento.competitor_id == Competitor.id)
        .join(Competicao, CompeticaoEvento.competicao_id == Competicao.id)
        .filter(CompeticaoEvento.id == competicao_id)
    )
    
    result = query.first()

    if result:
        return {
                "id": result.id,
                "value": result.value,
                "unidade": result.unidade,
                "competitor": {
                    "id": result.competitor_id,
                    "competitor_name": result.competitor_name,
                },
                "competicao": {
                    "id": result.competicao_id,
                    "descricao": result.competicao_descricao,
                    "modalidade": result.competicao_modalidade,
                }
            }
    return None


def get_competicao_evento(db: Session, competicao_id: int):
    return db.query(CompeticaoEvento).filter(CompeticaoEvento.id == competicao_id).first()


def get_competicoes_eventos(db: Session, skip: int = 0, limit: int = 100):
    
    eventos = []
    
    query = (
        db.query(
            CompeticaoEvento.id,
            CompeticaoEvento.value,
            CompeticaoEvento.unidade,
            Competitor.id.label("competitor_id"),
            Competitor.name.label("competitor_name"),
            Competicao.id.label("competicao_id"),
            Competicao.descricao.label("competicao_descricao"),
            Competicao.modalidade.label("competicao_modalidade"),
        )
        .join(Competitor, CompeticaoEvento.competitor_id == Competitor.id)
        .join(Competicao, CompeticaoEvento.competicao_id == Competicao.id)
        .offset(skip).limit(limit)
    )
    
    results = query.all()
    
    for result in results:
        eventos.append(        
            {
                "id": result.id,
                "value": result.value,
                "unidade": result.unidade,
                "competitor": {
                    "id": result.competitor_id,
                    "competitor_name": result.competitor_name,
                },
                "competicao": {
                    "id": result.competicao_id,
                    "descricao": result.competicao_descricao,
                    "modalidade": result.competicao_modalidade,
                },
            }
        )
    return eventos
    
    


def create_competicao_evento(db: Session, competicao: CompeticaoEventoCreate):
    
    # Verifica se o status da competição é 'FINALIZADO' e levanta uma exceção caso sim
    status_competicao = db.query(Competicao.status).filter(Competicao.id == competicao.competicao_id).first()
    if status_competicao and status_competicao[0] == 'FINALIZADO':
        raise HTTPException(status_code=404, detail="Competição já finalizada")
    
    # Verificando se o candidato da competição de "Dardo" possui 3 cadastros, caso sim, retorno 404 informando que não pode ter mais cadastros para aquele candidato
    modalidade = db.query(Competicao.modalidade).filter(Competicao.id == competicao.competicao_id).first()
    
    if modalidade and modalidade[0].lower() == "dardo":
        cadastro_competitor = db.query(CompeticaoEvento).filter(CompeticaoEvento.competitor_id == competicao.competitor_id).first()
        
        if cadastro_competitor:
            # Contar cadastros diretamente no banco
            count_cadastro_competitor = (
                db.query(CompeticaoEvento)
                .filter(
                    CompeticaoEvento.competitor_id == competicao.competitor_id,
                    CompeticaoEvento.competicao_id == competicao.competicao_id
                )
                .count()
            )
            if count_cadastro_competitor > 3:
                raise HTTPException(status_code=404, detail=f"Competidor já cadastrado mais de 3 vezes na modalidade Dardo")
            
        
    newCompeticao = CompeticaoEvento(competicao_id=competicao.competicao_id,
                                    competitor_id=competicao.competitor_id,
                                    value=competicao.value,
                                    unidade=competicao.unidade)
    
    db.add(newCompeticao)
    db.commit()
    db.refresh(newCompeticao)
    return newCompeticao

def delete_competicao_evento(db: Session, competicao_id: int):
    competicao_delete = get_competicao_evento(db, competicao_id)
    
    if competicao_delete:
        db.delete(competicao_delete)
        db.commit()
        
    return competicao_delete


def update_competicao_evento(db: Session, competicao_id: int, update_data: CompeticaoEventoCreate):
    competicao_evento_update = get_competicao_evento(db, competicao_id)

    if competicao_evento_update:
        competicao_evento_update.competicao_id = update_data.competicao_id
        competicao_evento_update.competitor_id = update_data.competitor_id
        competicao_evento_update.value = update_data.value
        competicao_evento_update.unidade = update_data.unidade
        
        db.commit()
        db.refresh(competicao_evento_update)
    return competicao_evento_update
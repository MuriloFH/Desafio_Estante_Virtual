from sqlalchemy.orm import Session
from sqlalchemy import Integer, cast
from fastapi import HTTPException
from app.models.competicaoEventoModel import CompeticaoEvento
from app.models.competicaoModel import Competicao
from app.models.competidorModel import Competitor

def get_competicao_evento_ranking_response(db: Session, competicao_id: int):
    competitors_ranking = []
    
    # Recuperar detalhes da competição
    competicao = db.query(Competicao).filter(Competicao.id == competicao_id).first()
    
    if not competicao:
        raise HTTPException(status_code=404, detail="Competição não encontrada")
    
    # Verificar tipo da competição
    tipo_competicao = competicao.modalidade.lower()
    if tipo_competicao not in ["dardo", "natação"]:
        raise HTTPException(status_code=400, detail="Modalidade inválida para ranking")

    # Query base para buscar os eventos e competidores da competição informada no parametro do get
    eventos_query = (
        db.query(CompeticaoEvento, Competitor.name, Competitor.identifier)
        .join(Competitor, CompeticaoEvento.competitor_id == Competitor.id)
        .filter(CompeticaoEvento.competicao_id == competicao_id)
    )
    
    # Filtrar os valores específicos por competidor (dardo = maior, natacao = menor)
    if tipo_competicao == "dardo":
        subquery = (
            eventos_query
            .group_by(CompeticaoEvento.competitor_id)
            .order_by(cast(CompeticaoEvento.value, Integer).desc())
        )
    elif tipo_competicao == "natação":
        subquery = (
            eventos_query
            .group_by(CompeticaoEvento.competitor_id)
            .order_by(cast(CompeticaoEvento.value, Integer).asc())
        )
    
    # Processar o resultado filtrado e formatar
    ranking_competicao_evento = subquery.all()
    
    # Estruturar os dados de ranking
    for count, evento in enumerate(ranking_competicao_evento):
        competitors_ranking.append(
            {
                "id": evento.CompeticaoEvento.competitor_id,
                "nome": evento.name,
                "identificador": evento.identifier,
                "valor": evento.CompeticaoEvento.value,
                "posicao": count + 1
            }  
        )

    # Estruturar o resultado final
    result = {
        "competicao-id": competicao.id,
        "competicao-descricao": competicao.descricao,
        "competicao-status": getattr(competicao, "status", "INDEFINIDO"),
        "competicao-modalidade": competicao.modalidade,
        "competitors-ranking": competitors_ranking
    }

    return result
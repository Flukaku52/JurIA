from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..services.legal_reference_service import search_legal_references

router = APIRouter()

class LegalReferenceResponse(BaseModel):
    id: str
    title: str
    content: str
    source: str
    type: str
    relevance_score: float
    publication_date: Optional[datetime] = None
    url: Optional[str] = None

@router.get("/search", response_model=List[LegalReferenceResponse])
async def search_references(
    query: str = Query(..., min_length=3, description="Termo de busca para referências legais"),
    source_type: Optional[str] = None,
    limit: int = 10,
    min_score: float = 0.5
):
    """
    Busca referências legais com base em um termo de pesquisa.
    
    - **query**: Termo de busca (mínimo 3 caracteres)
    - **source_type**: Filtrar por tipo de fonte (ex: "lei", "jurisprudencia", "doutrina")
    - **limit**: Número máximo de referências a serem retornadas (padrão: 10)
    - **min_score**: Pontuação mínima de relevância (entre 0 e 1, padrão: 0.5)
    """
    try:
        results = search_legal_references(query, source_type, limit, min_score)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar referências legais: {str(e)}")

@router.get("/{reference_id}")
async def get_reference_details(reference_id: str):
    """
    Retorna detalhes completos de uma referência legal específica.
    
    - **reference_id**: ID da referência legal
    """
    # Implementação a ser adicionada
    raise HTTPException(status_code=501, detail="Endpoint não implementado") 
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..services.international_law_service import search_international_law, get_singapore_legislation

router = APIRouter()

class InternationalLawResponse(BaseModel):
    id: str
    title: str
    content: str
    jurisdiction: str
    category: str
    source: str
    relevance_score: float
    publication_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    url: Optional[str] = None

class CustomsRegulationResponse(BaseModel):
    id: str
    country: str
    regulation_type: str
    title: str
    content: str
    hs_codes: Optional[List[str]] = None
    tariff_rate: Optional[float] = None
    requirements: Optional[List[str]] = None
    restrictions: Optional[List[str]] = None
    documentation: Optional[List[str]] = None
    relevance_score: float
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    url: Optional[str] = None

@router.get("/search", response_model=List[InternationalLawResponse])
async def search_international_laws(
    query: str = Query(..., min_length=3, description="Termo de busca para leis internacionais"),
    jurisdiction: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10,
    min_score: float = 0.5
):
    """
    Busca leis e regulamentações internacionais com base em um termo de pesquisa.
    
    - **query**: Termo de busca (mínimo 3 caracteres)
    - **jurisdiction**: Filtrar por jurisdição (ex: "singapore", "eu", "usa")
    - **category**: Filtrar por categoria (ex: "trade", "tax", "customs")
    - **limit**: Número máximo de resultados a retornar (padrão: 10)
    - **min_score**: Pontuação mínima de relevância (entre 0 e 1, padrão: 0.5)
    """
    try:
        results = search_international_law(query, jurisdiction, category, limit, min_score)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar leis internacionais: {str(e)}")

@router.get("/singapore", response_model=List[InternationalLawResponse])
async def get_singapore_regulations(
    category: Optional[str] = None,
    limit: int = 10
):
    """
    Retorna legislações específicas de Singapura.
    
    - **category**: Filtrar por categoria (ex: "business", "tax", "investment")
    - **limit**: Número máximo de resultados a retornar (padrão: 10)
    """
    try:
        results = get_singapore_legislation(category, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar legislação de Singapura: {str(e)}")

@router.get("/customs", response_model=List[CustomsRegulationResponse])
async def get_customs_regulations(
    country: Optional[str] = None,
    product_code: Optional[str] = None,
    regulation_type: Optional[str] = None,
    limit: int = 10
):
    """
    Retorna regulamentações alfandegárias.
    
    - **country**: Filtrar por país
    - **product_code**: Filtrar por código HS do produto
    - **regulation_type**: Filtrar por tipo de regulamentação (ex: "import", "export", "tariff")
    - **limit**: Número máximo de resultados a retornar (padrão: 10)
    """
    # Implementação a ser adicionada
    raise HTTPException(status_code=501, detail="Este endpoint será implementado em breve") 
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..services.recommendation_service import get_recommendations_for_user

router = APIRouter()

class RecommendationResponse(BaseModel):
    id: str
    title: str
    description: str
    source: str
    relevance_score: float
    created_at: datetime
    category: str
    url: Optional[str] = None

@router.get("/{user_id}", response_model=List[RecommendationResponse])
async def get_recommendations(
    user_id: str,
    limit: int = 10,
    category: Optional[str] = None
):
    """
    Retorna recomendações jurídicas personalizadas para um usuário específico.
    
    - **user_id**: ID do usuário para o qual as recomendações serão geradas
    - **limit**: Número máximo de recomendações a serem retornadas (padrão: 10)
    - **category**: Filtrar recomendações por categoria (opcional)
    """
    try:
        recommendations = get_recommendations_for_user(user_id, limit, category)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar recomendações: {str(e)}") 
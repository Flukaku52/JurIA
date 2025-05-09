from typing import List, Optional
from datetime import datetime
import uuid
from ..core.cache import get_cached_recommendations, cache_recommendations

# Dados mockados para desenvolvimento inicial
MOCK_RECOMMENDATIONS = [
    {
        "id": str(uuid.uuid4()),
        "title": "Atualização na Lei de Proteção de Dados",
        "description": "Novas diretrizes sobre proteção de dados pessoais em processos judiciais.",
        "source": "Legislação Federal",
        "relevance_score": 0.92,
        "created_at": datetime.now(),
        "category": "Proteção de Dados",
        "url": "https://example.com/lgpd-atualizacao"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Jurisprudência sobre Contratos Eletrônicos",
        "description": "Decisão recente do STJ estabelece precedente para validade de contratos eletrônicos.",
        "source": "STJ",
        "relevance_score": 0.87,
        "created_at": datetime.now(),
        "category": "Direito Digital",
        "url": "https://example.com/stj-contratos-eletronicos"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Artigo sobre Impactos da IA no Direito",
        "description": "Análise dos impactos da inteligência artificial na prática jurídica contemporânea.",
        "source": "Revista de Direito Digital",
        "relevance_score": 0.85,
        "created_at": datetime.now(),
        "category": "Tecnologia Jurídica",
        "url": "https://example.com/ia-direito-impactos"
    }
]

def get_recommendations_for_user(user_id: str, limit: int = 10, category: Optional[str] = None) -> List[dict]:
    """
    Retorna recomendações personalizadas para um usuário.
    
    Args:
        user_id: ID do usuário
        limit: Número máximo de recomendações
        category: Categoria para filtrar as recomendações
    
    Returns:
        Lista de recomendações
    """
    # Verificar se há recomendações em cache
    cached_recommendations = get_cached_recommendations(user_id)
    if cached_recommendations:
        recommendations = cached_recommendations
    else:
        # Em um ambiente real, aqui buscaríamos recomendações personalizadas
        # baseadas no perfil do usuário, histórico, etc.
        # Por enquanto, usamos dados mockados
        recommendations = MOCK_RECOMMENDATIONS
        
        # Armazenar em cache
        cache_recommendations(user_id, recommendations)
    
    # Aplicar filtro de categoria se solicitado
    if category:
        recommendations = [r for r in recommendations if r["category"] == category]
    
    # Limitar quantidade de resultados
    return recommendations[:limit] 
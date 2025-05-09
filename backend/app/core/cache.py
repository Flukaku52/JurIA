from typing import Dict, List, Optional, Any
import time
from datetime import datetime, timedelta

# Cache simples em memória
# Em um ambiente de produção, usaríamos Redis ou outra solução de cache distribuído
_RECOMMENDATION_CACHE: Dict[str, Dict[str, Any]] = {}
_LEGAL_REFERENCE_CACHE: Dict[str, Dict[str, Any]] = {}

# Configuração de tempo de expiração (em segundos)
RECOMMENDATION_CACHE_TTL = 3600  # 1 hora
LEGAL_REFERENCE_CACHE_TTL = 86400  # 24 horas

def get_cached_recommendations(user_id: str) -> Optional[List[dict]]:
    """
    Recupera recomendações em cache para um usuário.
    
    Args:
        user_id: ID do usuário
    
    Returns:
        Lista de recomendações ou None se não estiver em cache ou expirado
    """
    cache_entry = _RECOMMENDATION_CACHE.get(user_id)
    if not cache_entry:
        return None
        
    # Verificar se o cache expirou
    if time.time() - cache_entry["timestamp"] > RECOMMENDATION_CACHE_TTL:
        del _RECOMMENDATION_CACHE[user_id]
        return None
        
    return cache_entry["data"]

def cache_recommendations(user_id: str, recommendations: List[dict]) -> None:
    """
    Armazena recomendações em cache para um usuário.
    
    Args:
        user_id: ID do usuário
        recommendations: Lista de recomendações
    """
    _RECOMMENDATION_CACHE[user_id] = {
        "timestamp": time.time(),
        "data": recommendations
    }

def get_cached_legal_references(query: str, source_type: Optional[str] = None) -> Optional[List[dict]]:
    """
    Recupera referências legais em cache para uma consulta.
    
    Args:
        query: Termo de busca
        source_type: Tipo de fonte (opcional)
    
    Returns:
        Lista de referências legais ou None se não estiver em cache ou expirado
    """
    # Criar uma chave de cache que inclui a consulta e tipo de fonte (se especificado)
    cache_key = f"{query}:{source_type}" if source_type else query
    
    cache_entry = _LEGAL_REFERENCE_CACHE.get(cache_key)
    if not cache_entry:
        return None
        
    # Verificar se o cache expirou
    if time.time() - cache_entry["timestamp"] > LEGAL_REFERENCE_CACHE_TTL:
        del _LEGAL_REFERENCE_CACHE[cache_key]
        return None
        
    return cache_entry["data"]

def cache_legal_references(query: str, results: List[dict], source_type: Optional[str] = None) -> None:
    """
    Armazena referências legais em cache para uma consulta.
    
    Args:
        query: Termo de busca
        results: Lista de referências legais
        source_type: Tipo de fonte (opcional)
    """
    # Criar uma chave de cache que inclui a consulta e tipo de fonte (se especificado)
    cache_key = f"{query}:{source_type}" if source_type else query
    
    _LEGAL_REFERENCE_CACHE[cache_key] = {
        "timestamp": time.time(),
        "data": results
    }

def clear_user_cache(user_id: str) -> None:
    """
    Limpa o cache para um usuário específico.
    
    Args:
        user_id: ID do usuário
    """
    if user_id in _RECOMMENDATION_CACHE:
        del _RECOMMENDATION_CACHE[user_id]

def clear_all_caches() -> None:
    """
    Limpa todos os caches.
    """
    _RECOMMENDATION_CACHE.clear()
    _LEGAL_REFERENCE_CACHE.clear() 
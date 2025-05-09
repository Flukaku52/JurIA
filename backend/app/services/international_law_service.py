from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import random

# Dados mockados para desenvolvimento inicial - Direito Internacional
MOCK_INTERNATIONAL_LAWS = [
    {
        "id": str(uuid.uuid4()),
        "title": "Convenção de Viena sobre Direito dos Tratados",
        "content": "A Convenção de Viena sobre o Direito dos Tratados codifica as regras consuetudinárias que regem os acordos entre Estados. Estabelece normas para conclusão, interpretação e terminação de tratados.",
        "jurisdiction": "global",
        "category": "treaties",
        "source": "United Nations",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(1969, 5, 23),
        "last_updated": datetime(1980, 1, 27),
        "url": "https://treaties.un.org/doc/Publication/UNTS/Volume%201155/volume-1155-I-18232-English.pdf"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Acordo Geral sobre Tarifas e Comércio (GATT)",
        "content": "O GATT é um acordo multilateral que regula o comércio internacional, visando reduzir tarifas e outras barreiras comerciais entre os países signatários.",
        "jurisdiction": "global",
        "category": "trade",
        "source": "WTO",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(1947, 10, 30),
        "last_updated": datetime(1994, 4, 15),
        "url": "https://www.wto.org/english/docs_e/legal_e/gatt47_01_e.htm"
    }
]

# Dados mockados para desenvolvimento inicial - Legislação de Singapura
MOCK_SINGAPORE_LAWS = [
    {
        "id": str(uuid.uuid4()),
        "title": "Companies Act (Cap. 50)",
        "content": "A principal legislação que rege a formação, administração e regulação de empresas em Singapura. Estabelece requisitos para constituição de empresas, deveres de diretores, e procedimentos para dissolução.",
        "jurisdiction": "singapore",
        "category": "business",
        "source": "Singapore Statutes Online",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(1967, 12, 29),
        "last_updated": datetime(2020, 3, 25),
        "url": "https://sso.agc.gov.sg/Act/CoA1967"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Economic Expansion Incentives (Relief from Income Tax) Act",
        "content": "Provê incentivos fiscais para empresas que investem em setores específicos da economia de Singapura, incluindo isenções fiscais temporárias e créditos fiscais para pesquisa e desenvolvimento.",
        "jurisdiction": "singapore",
        "category": "tax",
        "source": "Singapore Statutes Online",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(1967, 2, 25),
        "last_updated": datetime(2018, 11, 12),
        "url": "https://sso.agc.gov.sg/Act/EERIA1967"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Customs Act (Cap. 70)",
        "content": "Regula a importação e exportação de mercadorias, o pagamento de tarifas aduaneiras e outros impostos, e estabelece os procedimentos de controle alfandegário em Singapura.",
        "jurisdiction": "singapore",
        "category": "customs",
        "source": "Singapore Statutes Online",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(1960, 6, 2),
        "last_updated": datetime(2020, 5, 15),
        "url": "https://sso.agc.gov.sg/Act/CA1960"
    }
]

def search_international_law(
    query: str,
    jurisdiction: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10,
    min_score: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Busca leis e regulamentações internacionais com base em um termo de pesquisa.
    
    Args:
        query: Termo de busca
        jurisdiction: Filtrar por jurisdição
        category: Filtrar por categoria
        limit: Número máximo de resultados
        min_score: Pontuação mínima de relevância
        
    Returns:
        Lista de leis internacionais que correspondem à pesquisa
    """
    # Combinar as leis internacionais com as de Singapura para busca
    all_laws = MOCK_INTERNATIONAL_LAWS + MOCK_SINGAPORE_LAWS
    
    # Em um ambiente real, aqui faríamos uma busca vetorial ou semântica
    # nos documentos jurídicos, usando embeddings ou outra técnica de IA
    
    # Por enquanto, simulamos a relevância com base em palavras-chave
    results = []
    query_terms = query.lower().split()
    
    for law in all_laws:
        # Filtrar por jurisdição, se especificada
        if jurisdiction and law["jurisdiction"] != jurisdiction.lower():
            continue
            
        # Filtrar por categoria, se especificada
        if category and law["category"] != category.lower():
            continue
            
        # Calcular pontuação de relevância simulada
        title_lower = law["title"].lower()
        content_lower = law["content"].lower()
        
        # Contagem simples de termos presentes
        term_matches = sum(1 for term in query_terms if term in title_lower or term in content_lower)
        
        # Dar mais peso para correspondências no título
        title_matches = sum(1 for term in query_terms if term in title_lower)
        
        # Pontuação baseada na proporção de termos correspondentes
        score = (term_matches / len(query_terms)) * 0.7 + (title_matches / len(query_terms)) * 0.3
        
        # Adicionar alguma aleatoriedade para simular variação nos resultados
        score = min(1.0, score + random.uniform(-0.1, 0.1))
        
        if score >= min_score:
            law_copy = law.copy()
            law_copy["relevance_score"] = score
            results.append(law_copy)
    
    # Ordenar por relevância
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Limitar o número de resultados
    return results[:limit]

def get_singapore_legislation(
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Retorna legislações específicas de Singapura.
    
    Args:
        category: Filtrar por categoria
        limit: Número máximo de resultados
        
    Returns:
        Lista de legislações de Singapura
    """
    # Filtrar por categoria, se especificada
    if category:
        results = [law for law in MOCK_SINGAPORE_LAWS if law["category"] == category.lower()]
    else:
        results = MOCK_SINGAPORE_LAWS.copy()
    
    # Adicionar pontuações de relevância aleatórias para ordenação
    for law in results:
        law["relevance_score"] = random.uniform(0.5, 1.0)
    
    # Ordenar por relevância
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Limitar o número de resultados
    return results[:limit] 
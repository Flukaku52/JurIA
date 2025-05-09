from typing import List, Optional
from datetime import datetime
import uuid
import random

# Dados mockados para desenvolvimento inicial
MOCK_LEGAL_REFERENCES = [
    {
        "id": str(uuid.uuid4()),
        "title": "Lei 13.709/2018 (LGPD)",
        "content": "Art. 1º Esta Lei dispõe sobre o tratamento de dados pessoais, inclusive nos meios digitais, por pessoa natural ou por pessoa jurídica de direito público ou privado, com o objetivo de proteger os direitos fundamentais de liberdade e de privacidade e o livre desenvolvimento da personalidade da pessoa natural.",
        "source": "Legislação Federal",
        "type": "lei",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(2018, 8, 14),
        "url": "http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Habeas Corpus 166.373/SP",
        "content": "EMENTA: HABEAS CORPUS. PROCESSUAL PENAL. PRISÃO PREVENTIVA. FUNDAMENTAÇÃO. GRAVIDADE ABSTRATA DO DELITO. INSUFICIÊNCIA. CIRCUNSTÂNCIAS DO CASO CONCRETO. AUSÊNCIA DE DEMONSTRAÇÃO. ORDEM CONCEDIDA.",
        "source": "STF",
        "type": "jurisprudencia",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(2021, 5, 18),
        "url": "https://example.com/stf-hc-166373"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Contratos Eletrônicos no Direito Brasileiro",
        "content": "O artigo analisa a validade dos contratos eletrônicos no ordenamento jurídico brasileiro, considerando a legislação vigente e a jurisprudência dos tribunais superiores.",
        "source": "Revista de Direito Civil",
        "type": "doutrina",
        "relevance_score": 0.0,  # Será calculado dinamicamente
        "publication_date": datetime(2022, 3, 10),
        "url": "https://example.com/revista-direito-civil/contratos-eletronicos"
    }
]

def search_legal_references(
    query: str,
    source_type: Optional[str] = None,
    limit: int = 10,
    min_score: float = 0.5
) -> List[dict]:
    """
    Busca referências legais com base em um termo de pesquisa.
    
    Args:
        query: Termo de busca
        source_type: Tipo de fonte (lei, jurisprudencia, doutrina)
        limit: Número máximo de resultados
        min_score: Pontuação mínima de relevância
        
    Returns:
        Lista de referências legais que correspondem à pesquisa
    """
    # Em um ambiente real, aqui faríamos uma busca vetorial ou semântica
    # nos documentos jurídicos, usando embeddings ou outra técnica de IA
    
    # Por enquanto, simulamos a relevância com base em palavras-chave no título e conteúdo
    results = []
    query_terms = query.lower().split()
    
    for reference in MOCK_LEGAL_REFERENCES:
        # Filtrar pelo tipo, se especificado
        if source_type and reference["type"] != source_type:
            continue
            
        # Calcular pontuação de relevância simulada
        title_lower = reference["title"].lower()
        content_lower = reference["content"].lower()
        
        # Contagem simples de termos presentes
        term_matches = sum(1 for term in query_terms if term in title_lower or term in content_lower)
        
        # Dar mais peso para correspondências no título
        title_matches = sum(1 for term in query_terms if term in title_lower)
        
        # Pontuação baseada na proporção de termos correspondentes e presença no título
        score = (term_matches / len(query_terms)) * 0.7 + (title_matches / len(query_terms)) * 0.3
        
        # Adicionar alguma aleatoriedade para simular variação nos resultados
        score = min(1.0, score + random.uniform(-0.1, 0.1))
        
        if score >= min_score:
            reference_copy = reference.copy()
            reference_copy["relevance_score"] = score
            results.append(reference_copy)
    
    # Ordenar por relevância
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Limitar o número de resultados
    return results[:limit] 
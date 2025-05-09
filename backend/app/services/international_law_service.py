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

# Dados mockados para desenvolvimento inicial - Regulamentações Alfandegárias
MOCK_CUSTOMS_REGULATIONS = [
    {
        "id": str(uuid.uuid4()),
        "country": "singapore",
        "regulation_type": "import",
        "title": "Procedimentos de Importação para Singapura",
        "content": "Todo importador deve obter um Número de Registro de Entidades Únicas (UEN) do Enterprise Singapore e ativar uma conta de Serviços de Rede de Comércio de Singapura (TradeNet). Os produtos importados estão sujeitos a verificação da Alfândega de Singapura e inspeção de conformidade com regulamentações técnicas.",
        "hs_codes": ["1000.00", "2000.00"],
        "tariff_rate": 0.07,
        "requirements": ["Licença de importação", "Declaração aduaneira", "Fatura comercial", "Conhecimento de embarque"],
        "restrictions": ["Produtos proibidos", "Mercadorias controladas"],
        "documentation": ["Formulário IN-1", "Certificado de origem"],
        "relevance_score": 0.0,
        "effective_date": datetime(2019, 1, 1),
        "expiration_date": None,
        "url": "https://www.customs.gov.sg/businesses/importing-goods/overview"
    },
    {
        "id": str(uuid.uuid4()),
        "country": "singapore",
        "regulation_type": "export",
        "title": "Regulamentações de Exportação de Singapura",
        "content": "Exportadores devem apresentar declaração de exportação através do TradeNet para todas as mercadorias. Certos tipos de produtos podem requerer licenças especiais. Produtos estratégicos e de dupla utilização estão sujeitos a controles adicionais.",
        "hs_codes": ["8471.30", "8517.12"],
        "tariff_rate": None,
        "requirements": ["Declaração de exportação", "Fatura comercial", "Lista de embalagem"],
        "restrictions": ["Tecnologia de dupla utilização", "Armas"],
        "documentation": ["Formulário EX-1", "Certificado de origem"],
        "relevance_score": 0.0,
        "effective_date": datetime(2018, 6, 15),
        "expiration_date": None,
        "url": "https://www.customs.gov.sg/businesses/exporting-goods/overview"
    },
    {
        "id": str(uuid.uuid4()),
        "country": "singapore",
        "regulation_type": "tariff",
        "title": "Tarifas e Impostos de Importação",
        "content": "Singapura aplica imposto sobre bens e serviços (GST) de 7% sobre a maioria dos produtos importados. Produtos como bebidas alcoólicas, tabaco, veículos motorizados e derivados de petróleo estão sujeitos a impostos adicionais. A maioria dos produtos não tem tarifas de importação.",
        "hs_codes": ["2203.00", "2204.10", "2402.20", "8703.21"],
        "tariff_rate": None,
        "requirements": ["Declaração de valor", "Classificação correta do código HS"],
        "restrictions": [],
        "documentation": ["Formulário GST-1"],
        "relevance_score": 0.0,
        "effective_date": datetime(2020, 2, 18),
        "expiration_date": None,
        "url": "https://www.customs.gov.sg/businesses/valuation-duties-taxes--fees/duties-and-dutiable-goods"
    },
    {
        "id": str(uuid.uuid4()),
        "country": "global",
        "regulation_type": "import",
        "title": "Sistema Harmonizado de Designação e Codificação de Mercadorias",
        "content": "O Sistema Harmonizado (HS) é uma nomenclatura internacional padronizada para classificação de produtos comercializados internacionalmente. Consiste em cerca de 5.000 grupos de produtos, cada um identificado por um código de 6 dígitos, organizado em estrutura lógica.",
        "hs_codes": [],
        "tariff_rate": None,
        "requirements": ["Classificação correta de mercadorias"],
        "restrictions": [],
        "documentation": ["Guia de classificação HS"],
        "relevance_score": 0.0,
        "effective_date": datetime(1988, 1, 1),
        "expiration_date": None,
        "url": "http://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx"
    }
]

# Dados mockados para análise de documentos
MOCK_DOCUMENT_ANALYSES = {
    "invoice": {
        "template_fields": ["número da fatura", "data de emissão", "valor total", "destinatário", "remetente", "descrição das mercadorias", "códigos HS"],
        "required_info": ["valor aduaneiro", "país de origem", "incoterms", "método de pagamento"],
        "compliance_checks": ["informações obrigatórias", "códigos HS corretos", "cálculo de impostos", "limitações/restrições"]
    },
    "bl": {
        "template_fields": ["número do conhecimento", "embarcador", "consignatário", "descrição das mercadorias", "quantidade", "porto de embarque", "porto de destino"],
        "required_info": ["documentos relacionados", "termos de frete", "notificações"],
        "compliance_checks": ["informações do transportador", "descrição de mercadorias", "volumes declarados"]
    },
    "packing_list": {
        "template_fields": ["referência", "data", "exportador", "importador", "detalhes de embalagem", "peso", "dimensões"],
        "required_info": ["marcações", "número de volumes", "peso bruto/líquido"],
        "compliance_checks": ["consistência com outros documentos", "especificações técnicas", "materiais de embalagem"]
    },
    "certificate_of_origin": {
        "template_fields": ["número do certificado", "exportador", "produtor", "importador", "descrição das mercadorias", "regras de origem", "declaração"],
        "required_info": ["critério de origem", "assinaturas autorizadas", "carimbos oficiais"],
        "compliance_checks": ["autoridade emissora reconhecida", "vigência", "autenticidade", "cumprimento das regras de origem"]
    }
}

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

def get_customs_regulations(
    country: Optional[str] = None,
    product_code: Optional[str] = None,
    regulation_type: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Retorna regulamentações alfandegárias filtradas por país, código de produto ou tipo.
    
    Args:
        country: Filtrar por país
        product_code: Filtrar por código HS do produto
        regulation_type: Filtrar por tipo de regulamentação
        limit: Número máximo de resultados
        
    Returns:
        Lista de regulamentações alfandegárias
    """
    results = []
    
    for regulation in MOCK_CUSTOMS_REGULATIONS:
        # Filtrar por país
        if country and regulation["country"] != country.lower():
            continue
            
        # Filtrar por tipo de regulamentação
        if regulation_type and regulation["regulation_type"] != regulation_type.lower():
            continue
            
        # Filtrar por código HS
        if product_code and regulation["hs_codes"] and not any(
            code.startswith(product_code.split('.')[0]) for code in regulation["hs_codes"]
        ):
            continue
            
        # Adicionar pontuação de relevância simulada
        regulation_copy = regulation.copy()
        regulation_copy["relevance_score"] = random.uniform(0.5, 1.0)
        
        # Dar prioridade a regulamentos com códigos HS correspondentes exatos
        if product_code and regulation["hs_codes"] and any(code == product_code for code in regulation["hs_codes"]):
            regulation_copy["relevance_score"] += 0.3
            
        results.append(regulation_copy)
    
    # Ordenar por relevância
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Limitar o número de resultados
    return results[:limit]

def analyze_customs_document(
    document_type: str,
    document_content: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analisa um documento alfandegário e fornece feedback sobre conformidade.
    
    Args:
        document_type: Tipo de documento (invoice, bl, packing_list, certificate_of_origin)
        document_content: Conteúdo extraído do documento em formato de dicionário
        
    Returns:
        Análise de conformidade e recomendações
    """
    if document_type not in MOCK_DOCUMENT_ANALYSES:
        return {
            "status": "error",
            "message": f"Tipo de documento não suportado: {document_type}",
            "supported_types": list(MOCK_DOCUMENT_ANALYSES.keys())
        }
    
    template = MOCK_DOCUMENT_ANALYSES[document_type]
    
    # Verificar campos obrigatórios
    missing_fields = [field for field in template["template_fields"] 
                     if field not in document_content or not document_content[field]]
    
    # Verificar informações adicionais necessárias
    missing_info = [info for info in template["required_info"] 
                   if info not in document_content or not document_content[info]]
    
    # Simular verificações de conformidade
    compliance_issues = []
    compliance_status = "compliant"
    
    # Simular problemas aleatórios para demonstração
    if random.random() < 0.3:
        compliance_issues.append("Informações inconsistentes com outras documentações")
        compliance_status = "warning"
        
    if random.random() < 0.2:
        compliance_issues.append("Classificação incorreta de código HS")
        compliance_status = "non_compliant"
        
    if document_type == "certificate_of_origin" and random.random() < 0.25:
        compliance_issues.append("Assinatura ou carimbo ausente/inválido")
        compliance_status = "non_compliant"
    
    # Compor resposta
    result = {
        "status": "success",
        "document_type": document_type,
        "analysis_timestamp": datetime.now().isoformat(),
        "missing_fields": missing_fields,
        "missing_info": missing_info,
        "compliance_status": compliance_status,
        "compliance_issues": compliance_issues,
        "recommendations": []
    }
    
    # Gerar recomendações com base nos problemas encontrados
    if missing_fields:
        result["recommendations"].append(f"Adicione os campos obrigatórios ausentes: {', '.join(missing_fields)}")
        
    if missing_info:
        result["recommendations"].append(f"Inclua as informações adicionais necessárias: {', '.join(missing_info)}")
        
    if compliance_issues:
        for issue in compliance_issues:
            result["recommendations"].append(f"Corrija o problema: {issue}")
    
    # Adicionar regulamentos relacionados
    if "hs_codes" in document_content and document_content["hs_codes"]:
        hs_code = document_content["hs_codes"][0] if isinstance(document_content["hs_codes"], list) else document_content["hs_codes"]
        country = document_content.get("country", "singapore")
        
        related_regulations = get_customs_regulations(
            country=country,
            product_code=hs_code,
            limit=2
        )
        
        if related_regulations:
            result["related_regulations"] = related_regulations
    
    return result 
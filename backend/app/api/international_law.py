from fastapi import APIRouter, HTTPException, Query, Body, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..services.international_law_service import (
    search_international_law, 
    get_singapore_legislation, 
    get_customs_regulations,
    analyze_customs_document
)

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

class DocumentAnalysisRequest(BaseModel):
    document_type: str
    document_content: Dict[str, Any]

class DocumentAnalysisResponse(BaseModel):
    status: str
    document_type: str
    analysis_timestamp: str
    missing_fields: List[str]
    missing_info: List[str]
    compliance_status: str
    compliance_issues: List[str]
    recommendations: List[str]
    related_regulations: Optional[List[CustomsRegulationResponse]] = None

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
async def get_customs_regulations_api(
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
    try:
        results = get_customs_regulations(country, product_code, regulation_type, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar regulamentações alfandegárias: {str(e)}")

@router.post("/analyze-document", response_model=DocumentAnalysisResponse)
async def analyze_document_api(
    document_data: DocumentAnalysisRequest = Body(..., description="Dados do documento a ser analisado")
):
    """
    Analisa um documento alfandegário e verifica sua conformidade com regulamentos.
    
    - **document_type**: Tipo de documento (ex: "invoice", "bl", "packing_list", "certificate_of_origin")
    - **document_content**: Conteúdo extraído do documento em formato JSON
    
    Retorna análise de conformidade, problemas identificados e recomendações.
    """
    try:
        result = analyze_customs_document(
            document_type=document_data.document_type,
            document_content=document_data.document_content
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao analisar documento: {str(e)}")

@router.post("/upload-document")
async def upload_document_analysis(
    document_type: str = Query(..., description="Tipo de documento (invoice, bl, packing_list, certificate_of_origin)"),
    file: UploadFile = File(..., description="Arquivo do documento a ser analisado (PDF, DOCX, XML)")
):
    """
    Recebe um documento via upload, extrai seu conteúdo e realiza análise de conformidade.
    
    - **document_type**: Tipo de documento sendo enviado
    - **file**: Arquivo do documento (formatos suportados: PDF, DOCX, XML)
    
    Nota: Esta é uma versão simulada que não realiza extração real do conteúdo.
    Em uma implementação completa, utilizaria OCR ou parsing específico para cada formato.
    """
    try:
        # Em uma implementação real, faria extração de texto do documento
        # Aqui, simulamos dados extraídos para demonstração
        
        # Verificar o tipo de arquivo
        file_extension = file.filename.split('.')[-1].lower()
        supported_extensions = ['pdf', 'docx', 'xml', 'json']
        
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Formato de arquivo não suportado. Formatos aceitos: {', '.join(supported_extensions)}"
            )
        
        # Dados simulados conforme o tipo de documento
        extracted_content = {}
        
        if document_type == "invoice":
            extracted_content = {
                "número da fatura": f"INV-{datetime.now().strftime('%Y%m%d')}-001",
                "data de emissão": datetime.now().isoformat(),
                "valor total": "5000.00",
                "destinatário": "Empresa XYZ Ltda.",
                "remetente": "Acme Global Trading",
                # Intencionalmente deixando alguns campos ausentes para demonstrar validação
                "códigos HS": ["8471.30", "8517.12"],
                "país de origem": "china"
            }
        elif document_type == "bl":
            extracted_content = {
                "número do conhecimento": f"BL-{datetime.now().strftime('%Y%m%d')}-001",
                "embarcador": "Acme Global Trading",
                "consignatário": "Empresa XYZ Ltda.",
                "descrição das mercadorias": "Equipamentos eletrônicos",
                "quantidade": "10 caixas",
                # Campos ausentes intencionalmente
            }
        elif document_type == "packing_list":
            extracted_content = {
                "referência": f"PL-{datetime.now().strftime('%Y%m%d')}-001",
                "data": datetime.now().isoformat(),
                "exportador": "Acme Global Trading",
                "importador": "Empresa XYZ Ltda.",
                "detalhes de embalagem": "10 caixas, 200kg total"
                # Campos ausentes intencionalmente
            }
        elif document_type == "certificate_of_origin":
            extracted_content = {
                "número do certificado": f"CO-{datetime.now().strftime('%Y%m%d')}-001",
                "exportador": "Acme Global Trading",
                "importador": "Empresa XYZ Ltda.",
                "descrição das mercadorias": "Equipamentos eletrônicos",
                "regras de origem": "Totalmente obtido"
                # Campos ausentes intencionalmente
            }
        else:
            return {
                "status": "error",
                "message": f"Tipo de documento não suportado: {document_type}",
                "supported_types": ["invoice", "bl", "packing_list", "certificate_of_origin"]
            }
        
        # Realizar a análise utilizando o serviço existente
        result = analyze_customs_document(
            document_type=document_type,
            document_content=extracted_content
        )
        
        # Adicionar informações do arquivo
        result["file_info"] = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": 0  # Em uma implementação real, teria o tamanho real
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}") 
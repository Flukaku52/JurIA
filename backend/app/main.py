from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Criação da aplicação FastAPI
app = FastAPI(
    title="JurIA API",
    description="API para o sistema de assistência jurídica com IA",
    version="0.1.0"
)

# Configuração de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Rota raiz da API que retorna uma mensagem de boas-vindas."""
    return {
        "message": "Bem-vindo à API do JurIA - Sistema de Assistência Jurídica com IA",
        "docs": "/docs",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Rota para verificação da saúde da aplicação."""
    return {"status": "healthy"}

# Ponto de entrada para execução direta
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
#!/bin/bash

# Cores para mensagens
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Iniciando JurIA...${NC}"

# Verificando dependências
echo -e "${YELLOW}Verificando dependências...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não encontrado. Por favor, instale-o para continuar.${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}NPM não encontrado. Por favor, instale o Node.js para continuar.${NC}"
    exit 1
fi

# Iniciando Backend
echo -e "${BLUE}Iniciando Backend...${NC}"
cd backend/app
python3 -m pip install -r ../requirements.txt
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Verificando se o backend iniciou corretamente
sleep 2
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}Backend iniciado com sucesso na porta 8000.${NC}"
else
    echo -e "${RED}Falha ao iniciar o backend.${NC}"
    exit 1
fi

# Voltando para a raiz do projeto
cd ../..

# Iniciando Frontend
echo -e "${BLUE}Iniciando Frontend...${NC}"
cd frontend
npm install
npm start &
FRONTEND_PID=$!

# Aguardando inicialização do frontend
sleep 5
if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}Frontend iniciado com sucesso na porta 3000.${NC}"
else
    echo -e "${RED}Falha ao iniciar o frontend.${NC}"
    kill $BACKEND_PID
    exit 1
fi

echo -e "${GREEN}JurIA iniciado com sucesso!${NC}"
echo -e "${BLUE}Backend:${NC} http://localhost:8000"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "${YELLOW}Para encerrar, pressione Ctrl+C${NC}"

# Função para encerrar processos ao finalizar
cleanup() {
    echo -e "${YELLOW}Encerrando JurIA...${NC}"
    kill $BACKEND_PID $FRONTEND_PID
    echo -e "${GREEN}Processos encerrados.${NC}"
    exit 0
}

# Registrar handler para SIGINT
trap cleanup SIGINT

# Manter o script em execução
wait 
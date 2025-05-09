export interface ConsultaCreate {
  pergunta: string;
  contexto?: string;
}

export interface ConsultaResponse {
  id: number;
  pergunta: string;
  contexto: string | null;
  resposta: string;
  data_criacao: string;
  data_resposta: string;
  status: string;
}

export interface ConsultaHistorico {
  id: number;
  pergunta: string;
  data_criacao: string;
  status: string;
  data_resposta: string | null;
} 
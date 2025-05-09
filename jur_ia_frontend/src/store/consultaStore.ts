import { create } from 'zustand';
import type { ConsultaCreate, ConsultaHistorico, ConsultaResponse } from '../types/consulta';
import { consultaService } from '../services/consultaService';

// Interface para o estado da store
interface ConsultaState {
  // Estado
  historicoConsultas: ConsultaHistorico[];
  consultaAtual: ConsultaResponse | null;
  loading: boolean;
  error: string | null;
  
  // Ações
  criarConsulta: (pergunta: string, contexto?: string) => Promise<ConsultaResponse>;
  carregarHistorico: () => Promise<void>;
  obterConsultaDetalhada: (id: number) => Promise<void>;
  limparConsultaAtual: () => void;
  limparErro: () => void;
}

// Estados iniciais 
const initialState = {
  historicoConsultas: [],
  consultaAtual: null,
  loading: false,
  error: null,
};

// Criação da store
export const useConsultaStore = create<ConsultaState>((set, get) => ({
  ...initialState,
  
  // Ações
  criarConsulta: async (pergunta: string, contexto?: string) => {
    set({ loading: true, error: null });
    
    try {
      const consultaData: ConsultaCreate = { 
        pergunta,
        ...(contexto ? { contexto } : {}) 
      };
      
      const resposta = await consultaService.criarConsulta(consultaData);
      
      const novoHistorico: ConsultaHistorico = {
        id: resposta.id,
        pergunta: resposta.pergunta,
        data_criacao: resposta.data_criacao,
        status: resposta.status,
        data_resposta: resposta.data_resposta
      };
      
      set({ 
        loading: false,
        consultaAtual: resposta,
        historicoConsultas: [novoHistorico, ...get().historicoConsultas]
      });
      
      return resposta;
    } catch (error: any) {
      const mensagemErro = error.response?.data?.detail || 'Erro ao criar consulta';
      set({ loading: false, error: mensagemErro });
      throw new Error(mensagemErro);
    }
  },
  
  carregarHistorico: async () => {
    set({ loading: true, error: null });
    
    try {
      const historico = await consultaService.listarConsultas();
      set({ historicoConsultas: historico, loading: false });
    } catch (error: any) {
      const mensagemErro = error.response?.data?.detail || 'Erro ao carregar histórico';
      set({ loading: false, error: mensagemErro });
    }
  },
  
  obterConsultaDetalhada: async (id: number) => {
    set({ loading: true, error: null });
    
    try {
      const consulta = await consultaService.obterConsulta(id);
      set({ consultaAtual: consulta, loading: false });
    } catch (error: any) {
      const mensagemErro = error.response?.data?.detail || 'Erro ao obter detalhes da consulta';
      set({ loading: false, error: mensagemErro });
    }
  },
  
  limparConsultaAtual: () => set({ consultaAtual: null }),
  
  limparErro: () => set({ error: null })
})); 
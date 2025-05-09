import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ConsultaPage from './ConsultaPage';
import * as consultaStoreModule from '../store/consultaStore';

// Mock do Zustand store
vi.mock('../store/consultaStore', () => ({
  useConsultaStore: vi.fn(),
}));

describe('ConsultaPage Component', () => {
  // Função auxiliar para mockagem do consultaStore
  const setupConsultaStoreMock = (overrides = {}) => {
    const mockStore = {
      consultaAtual: null,
      loading: false,
      error: null,
      criarConsulta: vi.fn().mockResolvedValue({}),
      limparErro: vi.fn(),
      ...overrides,
    };
    
    const mockedUseConsultaStore = consultaStoreModule.useConsultaStore as unknown as ReturnType<typeof vi.fn>;
    mockedUseConsultaStore.mockReturnValue(mockStore);
    
    return mockStore;
  };
  
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('deve renderizar o formulário de consulta corretamente', () => {
    setupConsultaStoreMock();
    
    render(<ConsultaPage />);
    
    // Verificar elementos do formulário
    expect(screen.getByText('Consulta Jurídica')).toBeInTheDocument();
    expect(screen.getByText('Faça sua pergunta e receba uma resposta baseada em conhecimento jurídico especializado.')).toBeInTheDocument();
    
    // Inputs
    expect(screen.getByLabelText(/sua pergunta jurídica/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/contexto adicional/i)).toBeInTheDocument();
    
    // Botão de envio
    expect(screen.getByRole('button', { name: /enviar consulta/i })).toBeInTheDocument();
  });
  
  it('deve mostrar indicador de carregamento durante o envio da consulta', async () => {
    setupConsultaStoreMock({ loading: true });
    
    render(<ConsultaPage />);
    
    // Verificar se o indicador de carregamento é exibido
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    
    // O botão deve estar desabilitado
    const botao = screen.getByRole('button');
    expect(botao).toBeDisabled();
  });
  
  it('deve mostrar mensagem de erro quando houver falha na consulta', () => {
    setupConsultaStoreMock({ 
      error: 'Erro na requisição: serviço indisponível' 
    });
    
    render(<ConsultaPage />);
    
    // Verificar se a mensagem de erro é exibida
    expect(screen.getByText('Erro na requisição: serviço indisponível')).toBeInTheDocument();
  });
  
  it('deve limpar o erro quando o usuário fechar o alerta', () => {
    const mockStore = setupConsultaStoreMock({ 
      error: 'Erro na requisição: serviço indisponível' 
    });
    
    render(<ConsultaPage />);
    
    // Verificar se a mensagem de erro é exibida
    expect(screen.getByText('Erro na requisição: serviço indisponível')).toBeInTheDocument();
    
    // Clicar no botão de fechar alerta
    fireEvent.click(screen.getByRole('button', { name: /close/i }));
    
    // Verificar se a função de limpar erro foi chamada
    expect(mockStore.limparErro).toHaveBeenCalled();
  });
  
  it('deve enviar a consulta ao submeter o formulário', async () => {
    const mockStore = setupConsultaStoreMock();
    
    render(<ConsultaPage />);
    
    // Preencher o formulário
    fireEvent.input(screen.getByLabelText(/sua pergunta jurídica/i), {
      target: { value: 'Quais são os requisitos para abertura de uma empresa?' }
    });
    
    fireEvent.input(screen.getByLabelText(/contexto adicional/i), {
      target: { value: 'Gostaria de abrir uma empresa de consultoria jurídica.' }
    });
    
    // Enviar o formulário
    fireEvent.click(screen.getByRole('button', { name: /enviar consulta/i }));
    
    // Verificar se a função de criar consulta foi chamada com os parâmetros corretos
    await waitFor(() => {
      expect(mockStore.criarConsulta).toHaveBeenCalledWith(
        'Quais são os requisitos para abertura de uma empresa?'
      );
    });
  });
  
  it('deve mostrar mensagem de validação se a pergunta for muito curta', async () => {
    setupConsultaStoreMock();
    
    render(<ConsultaPage />);
    
    // Preencher o formulário com pergunta inválida (muito curta)
    fireEvent.input(screen.getByLabelText(/sua pergunta jurídica/i), {
      target: { value: 'Oi' }
    });
    
    // Enviar o formulário
    fireEvent.click(screen.getByRole('button', { name: /enviar consulta/i }));
    
    // Verificar se a mensagem de validação aparece
    await waitFor(() => {
      expect(screen.getByText(/a pergunta deve ter pelo menos 5 caracteres/i)).toBeInTheDocument();
    });
  });
  
  it('deve mostrar a resposta quando a consulta for bem-sucedida', () => {
    const mockRespostaConsulta = {
      id: 1,
      pergunta: 'Quais são os requisitos para abertura de uma empresa?',
      contexto: 'Consultoria jurídica',
      resposta: 'Para abrir uma empresa, você precisa seguir os seguintes passos: 1. Registro na Junta Comercial...',
      data_criacao: '2023-05-20T14:30:00Z',
      data_resposta: '2023-05-20T14:31:00Z',
      status: 'respondida'
    };
    
    setupConsultaStoreMock({ 
      consultaAtual: mockRespostaConsulta 
    });
    
    render(<ConsultaPage />);
    
    // Verificar se a resposta é exibida
    expect(screen.getByText(/para abrir uma empresa, você precisa seguir/i)).toBeInTheDocument();
    expect(screen.getByText(/consulta realizada em:/i)).toBeInTheDocument();
  });
}); 
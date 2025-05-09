import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import HomePage from './HomePage';
import type { AuthContextType } from '../types/auth';

// Importação do hook antes do mock para evitar problemas de referência
import { useAuth } from '../contexts/AuthContext';

// Mockando o contexto de autenticação
vi.mock('../contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}));

describe('HomePage Component', () => {
  // Antes de cada teste, resetamos os mocks
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('deve renderizar corretamente para usuário não autenticado', () => {
    // Configurando o mock para simular usuário não autenticado
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
    } as unknown as AuthContextType);
    
    // Renderizando o componente
    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>
    );
    
    // Verificações de elementos principais
    expect(screen.getByText('JurIA')).toBeInTheDocument();
    expect(screen.getByText('Seu assistente jurídico com inteligência artificial')).toBeInTheDocument();
    
    // Verificação de recursos listados
    expect(screen.getByText('Consultas Jurídicas')).toBeInTheDocument();
    expect(screen.getByText('Pesquisa de Jurisprudência')).toBeInTheDocument();
    expect(screen.getByText('Histórico de Consultas')).toBeInTheDocument();
    
    // Verifica o botão principal para usuários não autenticados
    const mainButton = screen.getByText('Começar Agora');
    expect(mainButton).toBeInTheDocument();
    expect(mainButton.closest('a')).toHaveAttribute('href', '/login');
  });
  
  it('deve renderizar corretamente para usuário autenticado', () => {
    // Configurando o mock para simular usuário autenticado
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      isAuthenticated: true,
    } as unknown as AuthContextType);
    
    // Renderizando o componente
    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>
    );
    
    // Verificações de elementos principais
    expect(screen.getByText('JurIA')).toBeInTheDocument();
    expect(screen.getByText('Seu assistente jurídico com inteligência artificial')).toBeInTheDocument();
    
    // Verificação de recursos listados
    expect(screen.getByText('Consultas Jurídicas')).toBeInTheDocument();
    expect(screen.getByText('Pesquisa de Jurisprudência')).toBeInTheDocument();
    expect(screen.getByText('Histórico de Consultas')).toBeInTheDocument();
    
    // Verifica o botão principal para usuários autenticados
    const mainButton = screen.getByText('Nova Consulta');
    expect(mainButton).toBeInTheDocument();
    expect(mainButton.closest('a')).toHaveAttribute('href', '/consulta');
  });
  
  it('deve renderizar todas as características do sistema', () => {
    // Configurando o mock 
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
    } as unknown as AuthContextType);
    
    // Renderizando o componente
    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>
    );
    
    // Verificando as características listadas na página
    expect(screen.getByText('Como a JurIA pode ajudar você')).toBeInTheDocument();
    expect(screen.getByText('Uma solução completa para suas dúvidas jurídicas')).toBeInTheDocument();
    
    // Verificando descrições das características
    expect(screen.getByText('Tire suas dúvidas jurídicas com respostas rápidas e precisas baseadas em legislação atualizada.')).toBeInTheDocument();
    expect(screen.getByText('Encontre jurisprudências relevantes para seu caso com nossa ferramenta de busca inteligente.')).toBeInTheDocument();
    expect(screen.getByText('Acesse facilmente seu histórico de consultas anteriores para referência futura.')).toBeInTheDocument();
    
    // Verificando ícones (indiretamente, verificando suas seções)
    const sections = screen.getAllByRole('heading', { level: 3 });
    expect(sections).toHaveLength(3);
    expect(sections[0]).toHaveTextContent('Consultas Jurídicas');
    expect(sections[1]).toHaveTextContent('Pesquisa de Jurisprudência');
    expect(sections[2]).toHaveTextContent('Histórico de Consultas');
  });
}); 
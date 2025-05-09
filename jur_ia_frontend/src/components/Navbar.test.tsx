import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Navbar from './Navbar';
import type { AuthContextType, User } from '../types/auth';

// Importação do hook antes do mock para evitar problemas de referência
import { useAuth } from '../contexts/AuthContext';

// Mockando o contexto de autenticação
vi.mock('../contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}));

// Mock helpers para configurar o estado de autenticação
const mockAuthState = (isAuthenticated: boolean, user: User | null = null) => {
  const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
  mockUseAuth.mockReturnValue({
    isAuthenticated,
    user,
    token: isAuthenticated ? 'token-teste' : null,
    loading: false,
    error: null,
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
    clearError: vi.fn(),
  } as unknown as AuthContextType);
};

describe('Navbar Component', () => {
  
  // Antes de cada teste, resetamos os mocks
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('deve renderizar corretamente quando o usuário não está autenticado', () => {
    // Configurando o mock para simular usuário não autenticado
    mockAuthState(false);
    
    // Renderizando o componente dentro do BrowserRouter
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );
    
    // Verificações
    expect(screen.getByText('JurIA')).toBeInTheDocument();
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Registrar')).toBeInTheDocument();
    
    // Não deve mostrar links para usuários autenticados
    expect(screen.queryByText('Consulta')).not.toBeInTheDocument();
    expect(screen.queryByText('Histórico')).not.toBeInTheDocument();
    expect(screen.queryByText('Sair')).not.toBeInTheDocument();
  });
  
  it('deve renderizar corretamente quando o usuário está autenticado', () => {
    // Mock do usuário autenticado
    const mockUser: User = {
      id: 1,
      nome: 'Usuário Teste',
      email: 'teste@example.com',
      is_superuser: false,
      is_active: true,
      data_criacao: '2023-01-01T00:00:00Z'
    };
    
    // Configurando o mock para simular usuário autenticado
    mockAuthState(true, mockUser);
    
    // Renderizando o componente dentro do BrowserRouter
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );
    
    // Verificações
    expect(screen.getByText('JurIA')).toBeInTheDocument();
    expect(screen.getByText('Consulta')).toBeInTheDocument();
    expect(screen.getByText('Histórico')).toBeInTheDocument();
    expect(screen.getByText('Sair')).toBeInTheDocument();
    
    // Não deve mostrar links para usuários não autenticados
    expect(screen.queryByText('Login')).not.toBeInTheDocument();
    expect(screen.queryByText('Registrar')).not.toBeInTheDocument();
  });
}); 
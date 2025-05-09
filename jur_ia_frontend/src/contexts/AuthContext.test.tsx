import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AuthProvider, useAuth } from './AuthContext';
import type { LoginCredentials, User } from '../types/auth';
import { authService } from '../services/authService';

// Mock do serviço de autenticação
vi.mock('../services/authService', () => ({
  authService: {
    login: vi.fn(),
    register: vi.fn(),
    getCurrentUser: vi.fn(),
  },
}));

// Definição do tipo de erro estendido
interface ApiError extends Error {
  response?: {
    data?: {
      detail?: string;
    };
  };
}

// Componente para testar o hook useAuth
const TestComponent: React.FC = () => {
  const auth = useAuth();
  
  return (
    <div>
      <div data-testid="auth-state">
        {JSON.stringify({
          isAuthenticated: auth.isAuthenticated,
          loading: auth.loading,
          error: auth.error,
          user: auth.user,
        })}
      </div>
      <button onClick={() => auth.login({ username: 'test@example.com', password: 'password' })}>
        Login
      </button>
      <button onClick={() => auth.logout()}>
        Logout
      </button>
      <button onClick={() => auth.clearError()}>
        Clear Error
      </button>
    </div>
  );
};

describe('AuthContext', () => {
  // Antes de cada teste, limpar todos os mocks
  beforeEach(() => {
    vi.resetAllMocks();
    
    // Limpar localStorage
    localStorage.clear();
  });
  
  afterEach(() => {
    localStorage.clear();
    vi.resetAllMocks();
  });
  
  it('deve inicializar com valores padrão quando não há token no localStorage', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    const authState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
    
    expect(authState.isAuthenticated).toBe(false);
    expect(authState.loading).toBe(false);
    expect(authState.error).toBe(null);
    expect(authState.user).toBe(null);
  });
  
  it('deve inicializar com usuário e token do localStorage', () => {
    // Configurando localStorage com dados de teste
    const mockUser: User = {
      id: 1,
      nome: 'Usuário Teste',
      email: 'test@example.com',
      is_active: true,
      is_superuser: false,
      data_criacao: '2023-01-01T00:00:00Z'
    };
    
    localStorage.setItem('token', 'mock-token');
    localStorage.setItem('user', JSON.stringify(mockUser));
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    const authState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
    
    expect(authState.isAuthenticated).toBe(true);
    expect(authState.user).toEqual(mockUser);
  });
  
  it('deve fazer login e atualizar o estado corretamente', async () => {
    const mockUser: User = {
      id: 1,
      nome: 'Usuário Teste',
      email: 'test@example.com',
      is_active: true,
      is_superuser: false,
      data_criacao: '2023-01-01T00:00:00Z'
    };
    
    const mockLoginResponse = { access_token: 'mock-token', token_type: 'bearer' };
    
    // Configura os mocks para retornar os valores esperados
    (authService.login as ReturnType<typeof vi.fn>).mockResolvedValue(mockLoginResponse);
    (authService.getCurrentUser as ReturnType<typeof vi.fn>).mockResolvedValue(mockUser);
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Verifica estado inicial
    let authState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
    expect(authState.isAuthenticated).toBe(false);
    
    // Clica no botão de login
    await act(async () => {
      screen.getByText('Login').click();
    });
    
    // Aguarda as atualizações assíncronas
    await waitFor(() => {
      authState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
      expect(authState.isAuthenticated).toBe(true);
    });
    
    // Verifica se o serviço de login foi chamado corretamente
    expect(authService.login).toHaveBeenCalledWith({ 
      username: 'test@example.com', 
      password: 'password' 
    });
    
    // Verifica se o token e usuário foram salvos no localStorage
    expect(localStorage.getItem('token')).toBe('mock-token');
    expect(localStorage.getItem('user')).toBe(JSON.stringify(mockUser));
  });
  
  it('deve atualizar o estado com erro quando o login falha', async () => {
    // Configura o mock para retornar um erro
    const mockError = new Error('Credenciais inválidas') as ApiError;
    mockError.response = { data: { detail: 'Credenciais inválidas' } };
    
    (authService.login as ReturnType<typeof vi.fn>).mockRejectedValue(mockError);
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Clica no botão de login
    await act(async () => {
      screen.getByText('Login').click();
    });
    
    // Aguarda as atualizações assíncronas
    await waitFor(() => {
      const authState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
      expect(authState.error).toBe('Credenciais inválidas');
      expect(authState.isAuthenticated).toBe(false);
    });
  });
  
  it('deve fazer logout e limpar o estado e localStorage', async () => {
    // Configurando localStorage com dados de teste
    const mockUser: User = {
      id: 1,
      nome: 'Usuário Teste',
      email: 'test@example.com',
      is_active: true,
      is_superuser: false,
      data_criacao: '2023-01-01T00:00:00Z'
    };
    
    localStorage.setItem('token', 'mock-token');
    localStorage.setItem('user', JSON.stringify(mockUser));
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Verifica estado inicial (autenticado)
    const initialAuthState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
    expect(initialAuthState.isAuthenticated).toBe(true);
    
    // Clica no botão de logout dentro de act()
    await act(async () => {
      screen.getByText('Logout').click();
    });
    
    // Recarrega o estado após o logout
    const updatedAuthState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
    expect(updatedAuthState.isAuthenticated).toBe(false);
    expect(updatedAuthState.user).toBe(null);
    
    // Verifica se o localStorage foi limpo
    expect(localStorage.getItem('token')).toBe(null);
    expect(localStorage.getItem('user')).toBe(null);
  });
  
  it('deve limpar o erro quando clearError é chamado', async () => {
    // Configura o componente com um erro
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Simula um erro no estado diretamente
    await act(async () => {
      // Configura o mock para retornar um erro
      const mockError = new Error('Credenciais inválidas') as ApiError;
      mockError.response = { data: { detail: 'Credenciais inválidas' } };
      (authService.login as ReturnType<typeof vi.fn>).mockRejectedValue(mockError);
      
      // Clica no botão de login para gerar um erro
      screen.getByText('Login').click();
    });
    
    // Aguarda o erro aparecer
    await waitFor(() => {
      const errorState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
      expect(errorState.error).toBe('Credenciais inválidas');
    });
    
    // Clica no botão para limpar o erro dentro de act()
    await act(async () => {
      screen.getByText('Clear Error').click();
    });
    
    // Verifica se o erro foi limpo
    const clearedState = JSON.parse(screen.getByTestId('auth-state').textContent || '{}');
    expect(clearedState.error).toBe(null);
  });
}); 
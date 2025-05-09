import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import LoginPage from './LoginPage';
import type { AuthContextType } from '../types/auth';

// Mocks para o hook useNavigate do react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual as any,
    useNavigate: () => mockNavigate,
  };
});

// Importação do hook antes do mock para evitar problemas de referência
import { useAuth } from '../contexts/AuthContext';

// Mockando o contexto de autenticação
vi.mock('../contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}));

describe('LoginPage Component', () => {
  // Função auxiliar para mockagem do useAuth
  const setupAuthMock = (overrides = {}) => {
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      login: vi.fn(),
      clearError: vi.fn(),
      loading: false,
      error: null,
      ...overrides,
    } as unknown as AuthContextType);
    
    return mockUseAuth();
  };
  
  // Antes de cada teste, resetamos os mocks
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('deve renderizar o formulário de login corretamente', () => {
    setupAuthMock();
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Verificando os elementos do formulário
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
    expect(screen.getByText(/não tem uma conta\? registre-se/i)).toBeInTheDocument();
  });
  
  // O Material UI usa uma validação diferente que pode não exibir as mensagens
  // de erro da forma que estamos esperando nos testes
  it('deve verificar a validação dos campos', async () => {
    setupAuthMock();
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Clicar no botão de envio sem preencher os campos
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));
    
    // Verificamos que o formulário não permite envio com campos vazios
    const mockAuth = useAuth() as unknown as {login: ReturnType<typeof vi.fn>};
    await waitFor(() => {
      expect(mockAuth.login).not.toHaveBeenCalled();
    });
    
    // Verificamos que os campos são obrigatórios pelo atributo required
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/senha/i);
    
    expect(emailInput).toHaveAttribute('required');
    expect(passwordInput).toHaveAttribute('required');
  });
  
  it('deve mostrar erro quando o email é inválido', async () => {
    setupAuthMock();
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Preencher com email inválido
    fireEvent.input(screen.getByLabelText(/email/i), {
      target: { value: 'email-invalido' },
    });
    
    // Preencher senha (para focar no erro do email)
    fireEvent.input(screen.getByLabelText(/senha/i), {
      target: { value: 'senha123' },
    });
    
    // Clicar no botão de envio
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));
    
    // Aguardar mensagem de validação
    await waitFor(() => {
      expect(screen.getByText(/email inválido/i)).toBeInTheDocument();
    });
  });
  
  it('deve chamar a função de login ao submeter o formulário válido', async () => {
    const mockAuth = setupAuthMock();
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Preencher formulário corretamente
    fireEvent.input(screen.getByLabelText(/email/i), {
      target: { value: 'usuario@exemplo.com' },
    });
    
    fireEvent.input(screen.getByLabelText(/senha/i), {
      target: { value: 'senha123' },
    });
    
    // Clicar no botão de envio
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));
    
    // Verificar se login foi chamado com os dados corretos
    await waitFor(() => {
      expect(mockAuth.clearError).toHaveBeenCalled();
      expect(mockAuth.login).toHaveBeenCalledWith({
        username: 'usuario@exemplo.com',
        password: 'senha123',
      });
    });
  });
  
  it('deve mostrar mensagem de erro quando o login falha', async () => {
    setupAuthMock({
      error: 'Credenciais inválidas',
    });
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Verificar se o erro é exibido
    expect(screen.getByText('Credenciais inválidas')).toBeInTheDocument();
  });
  
  it('deve mostrar "Entrando..." quando o login está em andamento', () => {
    setupAuthMock({
      loading: true,
    });
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Verificar se o botão mostra o texto de carregamento
    expect(screen.getByRole('button', { name: /entrando/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrando/i })).toBeDisabled();
  });
  
  it('deve navegar para a página de registro quando o botão é clicado', () => {
    setupAuthMock();
    
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    
    // Clicar no botão de registro
    fireEvent.click(screen.getByText(/não tem uma conta\? registre-se/i));
    
    // Verificar se a função de navegação foi chamada
    expect(mockNavigate).toHaveBeenCalledWith('/register');
  });
}); 
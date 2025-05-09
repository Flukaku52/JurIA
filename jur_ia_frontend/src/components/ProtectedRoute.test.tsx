import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ProtectedRoute from './ProtectedRoute';
import type { AuthContextType } from '../types/auth';

// Importação do hook antes do mock para evitar problemas de referência
import { useAuth } from '../contexts/AuthContext';

// Mockando o contexto de autenticação
vi.mock('../contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}));

describe('ProtectedRoute Component', () => {
  
  // Antes de cada teste, resetamos os mocks
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  it('deve mostrar CircularProgress quando loading for true', () => {
    // Configurando o mock para simular carregamento
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
      loading: true,
    } as unknown as AuthContextType);
    
    // Renderizando o componente
    render(
      <MemoryRouter>
        <ProtectedRoute>
          <div>Conteúdo Protegido</div>
        </ProtectedRoute>
      </MemoryRouter>
    );
    
    // Verificando se o loader está sendo exibido
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    
    // Verificando que o conteúdo protegido não está sendo exibido
    expect(screen.queryByText('Conteúdo Protegido')).not.toBeInTheDocument();
  });
  
  it('deve redirecionar para /login quando não autenticado', () => {
    // Configurando o mock para simular não autenticado
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
      loading: false,
    } as unknown as AuthContextType);
    
    // Configurando um roteador de memória para capturar o redirecionamento
    render(
      <MemoryRouter initialEntries={['/protegido']}>
        <Routes>
          <Route 
            path="/protegido" 
            element={
              <ProtectedRoute>
                <div>Conteúdo Protegido</div>
              </ProtectedRoute>
            } 
          />
          <Route path="/login" element={<div>Página de Login</div>} />
        </Routes>
      </MemoryRouter>
    );
    
    // Verificando que houve redirecionamento para a página de login
    expect(screen.getByText('Página de Login')).toBeInTheDocument();
    
    // Verificando que o conteúdo protegido não está sendo exibido
    expect(screen.queryByText('Conteúdo Protegido')).not.toBeInTheDocument();
  });
  
  it('deve renderizar o conteúdo protegido quando autenticado', () => {
    // Configurando o mock para simular autenticado
    const mockUseAuth = useAuth as unknown as ReturnType<typeof vi.fn>;
    mockUseAuth.mockReturnValue({
      isAuthenticated: true,
      loading: false,
    } as unknown as AuthContextType);
    
    // Renderizando o componente
    render(
      <MemoryRouter>
        <ProtectedRoute>
          <div>Conteúdo Protegido</div>
        </ProtectedRoute>
      </MemoryRouter>
    );
    
    // Verificando que o conteúdo protegido está sendo exibido
    expect(screen.getByText('Conteúdo Protegido')).toBeInTheDocument();
  });
}); 
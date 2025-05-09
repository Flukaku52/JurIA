import React, { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import type { AuthContextType, AuthState, LoginCredentials, RegisterData, User } from '../types/auth';
import { authService } from '../services/authService';

// Valor padrão do contexto
const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  loading: false,
  error: null,
};

// Criação do contexto
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Hook personalizado para usar o contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};

type AuthProviderProps = {
  children: ReactNode;
};

// Componente provedor do contexto
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [state, setState] = useState<AuthState>(() => {
    // Verifica se há um token e um usuário no localStorage
    const token = localStorage.getItem('token');
    const userString = localStorage.getItem('user');
    const user = userString ? JSON.parse(userString) : null;

    return {
      ...initialState,
      isAuthenticated: !!token,
      token,
      user,
    };
  });

  // Efeito para carregar o usuário atual quando houver um token
  useEffect(() => {
    const loadUser = async () => {
      if (state.token && !state.user) {
        setState((prevState) => ({ ...prevState, loading: true }));
        try {
          const user = await authService.getCurrentUser();
          localStorage.setItem('user', JSON.stringify(user));
          setState((prevState) => ({ 
            ...prevState, 
            user, 
            isAuthenticated: true, 
            loading: false 
          }));
        } catch (error) {
          console.error('Erro ao carregar usuário:', error);
          // Se houver erro, faz logout para limpar o token inválido
          logout();
        }
      }
    };

    loadUser();
  }, [state.token]);

  // Função para fazer login
  const login = async (credentials: LoginCredentials) => {
    setState((prevState) => ({ ...prevState, loading: true, error: null }));
    try {
      const { access_token } = await authService.login(credentials);
      
      // Salva o token no localStorage
      localStorage.setItem('token', access_token);
      
      // Carrega as informações do usuário
      const user = await authService.getCurrentUser();
      localStorage.setItem('user', JSON.stringify(user));
      
      setState({
        isAuthenticated: true,
        user,
        token: access_token,
        loading: false,
        error: null,
      });
    } catch (error: any) {
      console.error('Erro de login:', error);
      setState((prevState) => ({ 
        ...prevState, 
        loading: false, 
        error: error.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.' 
      }));
    }
  };

  // Função para registrar um novo usuário
  const register = async (data: RegisterData) => {
    setState((prevState) => ({ ...prevState, loading: true, error: null }));
    try {
      const user = await authService.register(data);
      
      // Após o registro, faz login automaticamente
      await login({ username: data.email, password: data.password });
    } catch (error: any) {
      console.error('Erro de registro:', error);
      setState((prevState) => ({ 
        ...prevState, 
        loading: false, 
        error: error.response?.data?.detail || 'Erro ao registrar. Verifique seus dados.' 
      }));
    }
  };

  // Função para fazer logout
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setState({
      isAuthenticated: false,
      user: null,
      token: null,
      loading: false,
      error: null,
    });
  };

  // Função para limpar erros
  const clearError = () => {
    setState((prevState) => ({ ...prevState, error: null }));
  };

  const contextValue: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    clearError,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext; 
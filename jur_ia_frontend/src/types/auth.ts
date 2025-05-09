export interface User {
  id: number;
  nome: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  data_criacao: string;
}

export interface LoginCredentials {
  username: string; // É "username" porque o backend espera esse nome para o email
  password: string;
}

export interface RegisterData {
  nome: string;
  email: string;
  password: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
} 
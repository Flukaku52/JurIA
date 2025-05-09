import api from './api';
import type { LoginCredentials, RegisterData, TokenResponse, User } from '../types/auth';

export const authService = {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await api.post<TokenResponse>('/usuario/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/usuario', data);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/usuario/me');
    return response.data;
  },
}; 
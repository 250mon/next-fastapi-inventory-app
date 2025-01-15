import api from './axios';
import { User, LoginCredentials, RegisterCredentials, AuthResponse } from '../types/auth';

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      const response = await api.post<AuthResponse>('/auth/login', credentials);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  },

  register: async (credentials: RegisterCredentials): Promise<User> => {
    if (credentials.password !== credentials.confirm_password) {
      throw new Error('Passwords do not match');
    }

    try {
      const { confirm_password, ...registerData } = credentials;
      const response = await api.post<User>('/auth/register', registerData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  isAuthenticated: (): boolean => {
    const token = localStorage.getItem('token');
    if (!token) return false;

    // You could add token expiration check here if needed
    return true;
  },

  getCurrentUser: (): User | null => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }
}; 
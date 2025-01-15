import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, LoginCredentials, RegisterCredentials } from '../types/auth';
import { authService } from '@/lib/api/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (credentials: RegisterCredentials) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export const useAuth = create<AuthState>()(
  persist(
    (set, get) => ({
      user: authService.getCurrentUser(),
      token: localStorage.getItem('token'),
      isLoading: false,
      error: null,
      isAuthenticated: authService.isAuthenticated(),

      login: async (credentials) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authService.login(credentials);
          set({
            token: response.token,
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.message,
            isLoading: false,
            isAuthenticated: false,
          });
        }
      },

      register: async (credentials) => {
        set({ isLoading: true, error: null });
        try {
          await authService.register(credentials);
          // Automatically log in after successful registration
          await get().login({
            email: credentials.email,
            password: credentials.password,
          });
        } catch (error: any) {
          set({
            error: error.message,
            isLoading: false,
            isAuthenticated: false,
          });
        }
      },

      logout: () => {
        authService.logout();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        });
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
); 
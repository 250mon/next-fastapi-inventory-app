export interface User {
  id: number;
  email: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials extends LoginCredentials {
  confirm_password: string;
}

export interface AuthResponse {
  token: string;
  token_type: string;
  user: User;
} 
import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { authConfig } from "@/auth.config";
import { z } from "zod";
import type { User, AuthResponse, LoginCredentials, RegisterCredentials } from "@/lib/definitions";
// import bcrypt from "bcrypt";
import { serverApi } from '@/lib/api/server'
import { AuthError } from "next-auth";
import api from '@/lib/api/axios'

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;

if (!API_URL) {
  throw new Error('NEXT_PUBLIC_BACKEND_API_URL is not defined');
}

interface FastAPIUser {
  id: number;
  email: string;
  token: string;
}

async function getUser(credentials: LoginCredentials): Promise<User | undefined> {
  try {
    // const response = await serverApi.auth.login(credentials);
    // const response = await api.post<AuthResponse>('/auth/login', credentials);
    const response = {
      data: {
        user: {
          id: '1',
          email: 'test@test.com',
          name: 'Test User',
        }
      }
    }
    console.log("User fetched:", response.data.user);
    return response.data.user;
  } catch (error) {
    console.error("Failed to fetch user:", error);
    throw new Error("Failed to fetch user.");
  }
}

export const { auth, signIn, signOut } = NextAuth({
  ...authConfig,
  providers: [
    Credentials({
      async authorize(credentials) {
        console.log('NextAuth: Starting authorize function');
        try {
          console.log('NextAuth: Credentials received:', {
            email: credentials?.email,
            hasPassword: !!credentials?.password,
          });

          console.log('NextAuth: Making request to FastAPI');
          const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials),
          });

          console.log('NextAuth: Response status:', response.status);

          if (!response.ok) {
            console.log('NextAuth: Login failed with status:', response.status);
            return null;
          }

          const data = await response.json();
          console.log('NextAuth: Login successful, data:', data);
          
          // Return user object with token
          return {
            id: data.user.id,
            email: data.user.email,
            accessToken: data.token,
          };
        } catch (error) {
          console.error('NextAuth: Authentication error:', {
            name: error instanceof Error ? error.name : 'Unknown',
            message: error instanceof Error ? error.message : String(error),
            stack: error instanceof Error ? error.stack : undefined,
          });
          return null;
        }
      },
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      console.log('NextAuth: JWT Callback', { 
        hasUser: !!user, 
        hasToken: !!token 
      });
      if (user) {
        token.accessToken = user.accessToken;
        token.email = user.email;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      console.log('NextAuth: Session Callback', { 
        hasSession: !!session, 
        hasToken: !!token 
      });
      if (token) {
        session.user = {
          id: token.id as number,
          email: token.email as string,
        };
        session.accessToken = token.accessToken as string;
      }
      return session;
    },
  },
});

export const register = async (credentials: RegisterCredentials): Promise<User> => {
  if (credentials.password !== credentials.confirm_password) {
    throw new Error('Passwords do not match');
  }

  try {
    const response = await api.post<User>('/auth/register', credentials);
    return response.data;
  } catch (error) {
    throw new Error('Registration failed');
  }
}


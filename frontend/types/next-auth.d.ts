import 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      id: number;
      email: string;
    };
    accessToken: string;
  }

  interface User {
    id: number;
    email: string;
    accessToken: string;
  }

  interface JWT {
    id: number;
    email: string;
    accessToken: string;
  }
} 
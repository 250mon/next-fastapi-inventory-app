const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;

if (!API_URL) {
  throw new Error('NEXT_PUBLIC_BACKEND_API_URL is not defined');
}

interface FetchOptions extends RequestInit {
  token?: string;
}

async function fetchApi(endpoint: string, options: FetchOptions = {}) {
  const { token, ...fetchOptions } = options;
  const headers = new Headers(options.headers);

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  headers.set('Content-Type', 'application/json');

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'An error occurred');
  }

  return data;
}

export const serverApi = {
  auth: {
    login: async (credentials: { email: string; password: string }) => {
      return fetchApi('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
    },
    register: async (credentials: { email: string; password: string }) => {
      return fetchApi('/auth/register', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
    },
  },
  items: {
    getAll: async (token: string) => {
      return fetchApi('/items/', { token });
    },
    getById: async (id: number, token: string) => {
      return fetchApi(`/items/${id}`, { token });
    },
    create: async (data: any, token: string) => {
      return fetchApi('/items/', {
        method: 'POST',
        body: JSON.stringify(data),
        token,
      });
    },
    update: async (id: number, data: any, token: string) => {
      return fetchApi(`/items/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
        token,
      });
    },
    delete: async (id: number, token: string) => {
      return fetchApi(`/items/${id}`, {
        method: 'DELETE',
        token,
      });
    },
  },
  transactions: {
    getAll: async (token: string) => {
      return fetchApi('/transactions/', { token });
    },
    create: async (data: any, token: string) => {
      return fetchApi('/transactions/', {
        method: 'POST',
        body: JSON.stringify(data),
        token,
      });
    },
  },
}; 
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type AuthState = {
  user: null | {
    id: string;
    email: string;
    fullName: string;
  };
  accessToken: string | null;
  refreshToken: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const useAuth = create<AuthState>(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,

      login: async (email: string, password: string) => {
        const response = await fetch(`${API_URL}/api/v1/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            username: email,
            password: password,
          }),
        });

        if (!response.ok) {
          throw new Error('Login failed');
        }

        const data = await response.json();
        set({
          accessToken: data.access_token,
          refreshToken: data.refresh_token,
        });

        // Fetch user data
        const userResponse = await fetch(`${API_URL}/api/v1/users/me`, {
          headers: {
            Authorization: `Bearer ${data.access_token}`,
          },
        });

        if (!userResponse.ok) {
          throw new Error('Failed to fetch user data');
        }

        const userData = await userResponse.json();
        set({ user: userData });
      },

      register: async (email: string, password: string, fullName: string) => {
        const response = await fetch(`${API_URL}/api/v1/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email,
            password,
            full_name: fullName,
          }),
        });

        if (!response.ok) {
          throw new Error('Registration failed');
        }
      },

      logout: () => {
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
        });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
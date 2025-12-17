import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import type { User, Usage } from '../types';
import { apiService } from '../services/api';

interface AuthContextType {
  user: User | null;
  usage: Usage;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateUsage: (chars: number) => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [usage, setUsage] = useState<Usage>({ used: 0, limit: 10000 });

  useEffect(() => {
    // Check for stored user session
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        setUser(userData);
        apiService.setApiKey(userData.apiKey);
        
        // Load usage
        const storedUsage = localStorage.getItem('usage');
        if (storedUsage) {
          setUsage(JSON.parse(storedUsage));
        }
      } catch (error) {
        console.error('Failed to restore session:', error);
        localStorage.removeItem('user');
      }
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const data = await apiService.login(email, password);
      const userData: User = {
        id: data.user.id,
        email: data.user.email,
        name: data.user.name,
        plan: data.user.plan || 'free',
        apiKey: data.apiKey,
      };
      
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      apiService.setApiKey(userData.apiKey);

      // Set usage limits based on plan
      const limits = { free: 10000, pro: 1000000, enterprise: Infinity };
      setUsage({ used: data.usage?.used || 0, limit: limits[userData.plan] });
    } catch (error) {
      throw error;
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    try {
      const data = await apiService.signup(name, email, password);
      const userData: User = {
        id: data.user.id,
        email: data.user.email,
        name: data.user.name,
        plan: 'free',
        apiKey: data.apiKey,
      };
      
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      apiService.setApiKey(userData.apiKey);
      setUsage({ used: 0, limit: 10000 });
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      localStorage.removeItem('user');
      localStorage.removeItem('usage');
      apiService.setApiKey(undefined);
      setUsage({ used: 0, limit: 10000 });
    }
  };

  const updateUsage = (chars: number) => {
    const newUsage = { ...usage, used: usage.used + chars };
    setUsage(newUsage);
    localStorage.setItem('usage', JSON.stringify(newUsage));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        usage,
        login,
        signup,
        logout,
        updateUsage,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

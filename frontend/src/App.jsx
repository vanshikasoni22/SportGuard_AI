import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';

export default function App() {
  const [user, setUser] = useState(null);

  // Restore session on mount
  useEffect(() => {
    const stored = localStorage.getItem('sg_user');
    const token  = localStorage.getItem('sg_token');
    if (stored && token) {
      try { setUser(JSON.parse(stored)); } catch { /* ignore */ }
    }
  }, []);

  const handleAuth = (userData) => setUser(userData);

  const handleLogout = () => {
    localStorage.removeItem('sg_token');
    localStorage.removeItem('sg_user');
    setUser(null);
  };

  if (!user) return <LoginPage onAuth={handleAuth} />;
  return <Dashboard user={user} onLogout={handleLogout} />;
}

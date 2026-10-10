import React, { useState, useEffect } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

export default function App() {
  const [currentPage, setCurrentPage] = useState('login'); // 'login' | 'register' | 'dashboard'
  const [user, setUser] = useState(null);

  // Check stored credentials on mount
  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id');
    const storedGmail = localStorage.getItem('user_email');
    const storedUsername = localStorage.getItem('user_username');

    if (storedUserId) {
      setUser({
        userId: Number(storedUserId),
        gmail: storedGmail || `User #${storedUserId}`,
        username: storedUsername || '',
      });
      setCurrentPage('dashboard');
    }
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setCurrentPage('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_username');
    setUser(null);
    setCurrentPage('login');
  };

  if (currentPage === 'dashboard' && user) {
    return <Dashboard user={user} onLogout={handleLogout} />;
  }

  if (currentPage === 'register') {
    return (
      <Register
        onNavigateToLogin={() => setCurrentPage('login')}
        onRegisterSuccess={() => setCurrentPage('login')}
      />
    );
  }

  return (
    <Login
      onLoginSuccess={handleLoginSuccess}
      onNavigateToRegister={() => setCurrentPage('register')}
    />
  );
}

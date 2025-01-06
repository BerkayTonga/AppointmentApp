import React, { useState, useEffect } from 'react';
import './App.css';
import LoginScreen from './LoginScreen';
import RegisterScreen from './RegisterScreen';
import CalendarScreen from './CalendarScreen';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <div className="App">
      {isAuthenticated ? (
        <CalendarScreen user={user} onLogout={handleLogout} />
      ) : isRegistering ? (
        <RegisterScreen onBack={() => setIsRegistering(false)} />
      ) : (
        <LoginScreen onLogin={handleLogin} onRegister={() => setIsRegistering(true)} />
      )}
    </div>
  );
}

export default App;
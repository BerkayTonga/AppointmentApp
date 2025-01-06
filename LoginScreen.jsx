import React, { useState } from 'react';
import axios from 'axios';

function LoginScreen({ onLogin, onRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/login', { username, password });
      if (response.data.success) {
        onLogin(response.data.user);
      } else {
        alert('Login failed!');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="login-screen">
      <h1>Login</h1>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      <button onClick={onRegister}>Register</button>
    </div>
  );
}

export default LoginScreen;
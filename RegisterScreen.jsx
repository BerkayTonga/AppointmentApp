import React, { useState } from 'react';
import axios from 'axios';

function RegisterScreen({ onBack }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');

  const handleRegister = async () => {
    try {
      const response = await axios.post('/api/register', { username, password, email });
      if (response.data.success) {
        alert('Registration successful! You can now log in.');
        onBack();
      } else {
        alert('Registration failed!');
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  return (
    <div className="register-screen">
      <h1>Register</h1>
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
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
      <button onClick={onBack}>Back</button>
    </div>
  );
}

export default RegisterScreen;
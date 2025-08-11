import { useState,useEffect  } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // call Django endpoint that sets the csrftoken cookie
    api.get('csrf/');
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const csrfToken = getCookie('csrftoken');
      const response = await api.post(
        'accounts/login/',
        { username, password },
        { headers: { 'X-CSRFToken': csrfToken } }
      );
      console.log('Login success:', response.data);
      navigate('/exams/1');
    } catch (err) {
      console.error('Login error:', err);
      setError('Invalid username or password');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{ display: 'block', marginBottom: 10, width: '100%' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: 'block', marginBottom: 10, width: '100%' }}
        />
        <button type="submit" style={{ width: '100%' }}>
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;

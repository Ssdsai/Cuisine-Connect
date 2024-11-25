import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../Login/login.css";
import Footer from '../Foooter/footer';

function Login({ onSuccessfulLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous error message

    const payload = {
      email,
      password,
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload), // Convert payload to JSON string
      });

      const result = await response.json();

      if (response.ok) {
        const { user_id } = result; // Assuming backend returns user_id
        localStorage.setItem("isLoggedIn", "true"); // Store logged-in state
        localStorage.setItem("userEmail", email); // Save email to local storage
        localStorage.setItem("userId", user_id); // Save user_id to local storage
        console.log("User ID:", user_id); // Log the user_id to the console

        if (onSuccessfulLogin) {
          onSuccessfulLogin(); // Notify parent component
        } else {
          navigate("/"); // Redirect to home page if logged in
        }
      } else {
        setError(result.message); // Show error message from backend
      }
    } catch (error) {
      setError('An error occurred while logging in'); // Generic error message
      console.error("Login error:", error); // Log the error for debugging
    }
  };

  return (
      <div className="login-container">
        <h1>Login</h1>
        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Enter your email</label>
            <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Enter your password</label>
            <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
          </div>
          <button type="submit">Login</button>
          {error && <p className="error-message">{error}</p>} {/* Display error message if exists */}
        </form>
        <p className="create-account">
          Don't have an account? <a href="/create">Create one</a>
        </p>
        <Footer />
      </div>
  );
}

export default Login;
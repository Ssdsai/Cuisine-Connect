import React, { useState } from 'react';
import "../Create-Account/create.css";
import { useNavigate } from 'react-router-dom'; // Importing useNavigate for redirection
import Footer from '../Foooter/footer';

function CreateAccount() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate(); // Initialize navigate

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    setError('');

    const payload = {
      name,
      email,
      password,
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/create-account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload), // Convert payload to JSON string
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        // Redirect to /login if the account creation is successful
        navigate("/login"); // Redirect to login page
      } else {
        setError(result.message);
      }
    } catch (error) {
      setError('An error occurred while creating the account');
      console.error("Account creation error:", error); // Log the error for debugging
    }
  };

  return (
      <div className="create-account-container">
        <h1>Create Account</h1>
        <form onSubmit={handleCreateAccount} className="create-account-form">
          <div className="form-group">
            <label htmlFor="name">Enter your name</label>
            <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
            />
          </div>
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
          {error && <p className="error-message">{error}</p>}
          <button type="submit">Create Account</button>
        </form>
        <Footer />
      </div>
  );
}

export default CreateAccount;
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    console.log("Login-Daten:", { email, password });

    if (!email || !password) {
      setMessage("Please fill in both email and password");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password }),
        mode: 'cors'
      });

      if (!response.ok) {
        throw new Error("Login failed!");
      }

      const data = await response.json();
      console.log("Server-Antwort:", data);
      setMessage(data.message);

      if (data.success) {
        navigate("/");
      }
    } catch (error) {
      setMessage("Error: " + error.message);
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <p className="welcome-message">Welcome Back!</p>
        <h1 className="login-slogan">
          Log in to <span className="highlight">clop.board</span>
        </h1>
      </div>
      <div className="login-right">
        <form className="login-form" onSubmit={handleLogin}>
          <div className="input-group">
            <input
              type="text"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="input-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button className="login-button" type="submit">
            Login
          </button>
        </form>
        <p>
          Don't have an account?{" "}
          <a href="/signup" className="signup-link">
            Sign up
          </a>
        </p>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default LoginPage;

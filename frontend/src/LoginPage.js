import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";
import { AuthContext } from "./AuthContext";

function LoginPage() {
  //get login function from AuthContext
  const { login } = useContext(AuthContext);
  //State variables to store user input and messages
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  // Function to handle the login form submission
  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent page reload

    console.log("Login-Daten:", { email, password });

    // Ensure both email and password fields are filled
    if (!email || !password) {
      setMessage("Please fill in both email and password");
      return;
    }

    // Call the login function from AuthContext
    const result = await login(email, password);

    if(result.success){
      console.log("Login erfolgreich, weiterleiten...");
      navigate("/"); // Redirect to the home page
    }
    else{
      setMessage(result.message);
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
          <button className="login2-button" type="submit">
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

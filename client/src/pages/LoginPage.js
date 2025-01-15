import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";

const LoginPage = () => {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try{
      const response = await fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password}),
      });
      const data = await response.json();
      if(data.success){
        alert("Login successful!");
        navigate("/home");
      }
      else{
        alert("Error: " + data.message);
      }
    }
    catch(error){
      alert("An error occured: " + error.message);
    }
  };

  return (
    <div className="login-container">
      <h1 className="login-title">Welcome to our cinema!</h1>
      <p className="login-description">Please enter your username and your password</p>
      <form className="login-form" onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text"
                 name="username"
                 value={username}
                 onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <br />
        <label>
          Password:
          <input type="password"
                 name="password"
                 value={password}
                 onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <br />
        <button type="submit" className="login-button">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;

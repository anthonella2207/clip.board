import React, { useState } from "react";
import "./SignupPage.css";

const SignupPage = () => {
  const [formData, setFormData] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (data.success) {
        alert("Account created successfully!");
      } else {
        alert("Error: " + data.message);
      }
    } catch (error) {
      alert("An error occurred: " + error.message);
    }
  };

  return (
    <div className="signup-container">
      {/* Sección Izquierda */}
      <div className="signup-left">
        <h3 className="join-for-free">JOIN FOR FREE</h3>
        <h1 className="signup-slogan">
          Experience Movies Like <span className="highlight">Never Before!</span>
        </h1>
      </div>

      {/* Sección Derecha */}
      <div className="signup-right">
        <h2>Create new account.</h2>
        <form className="signup-form" onSubmit={handleSubmit}>
          <div className="input-group">
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
            <div className="name-fields">
                <input
                    type="text"
                    name="firstName"
                    placeholder="First Name"
                    required
                />
                <input
                    type="text"
                    name="lastName"
                    placeholder="Last Name"
                    required
                />
            </div>
            <div className="input-group">
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="signup-button">Create Account</button>
        </form>
        <p>
          Already a member? <a href="/login" className="login-link">Log In</a>
        </p>
      </div>
    </div>
  );
};

export default SignupPage;

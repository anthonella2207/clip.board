import React, { useState } from "react";
import "./SignupPage.css";

function SignupPage(){
  const[first_name, setFirst_name] = useState("");
  const[last_name, setLast_name] = useState("");
  const[email, setEmail] = useState("");
  const[password, setPassword] = useState("");
  const[message, setMessage] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();

    console.log("Signup-Daten:", { first_name, last_name, email, password });

    const response = await fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        vorname: first_name,
        nachname: last_name,
        email,
        password}),
    });

    const data = await response.json();
    setMessage(data.message);

    if (data.success) {
      console.log("✅ Signup erfolgreich, Logging wird erstellt...");
      await fetch("http://127.0.0.1:5000/add_log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "User signed up",
          user_id: data.user_id
        }),
      });
    }
  };

  return (
    <div className="signup-container">  {/* ✅ Hauptcontainer für das Layout */}
      {/* Linke Sektion */}
      <div className="signup-left">
        <p className="join-for-free">Join for free</p>
        <h1 className="signup-slogan">
          Create an account on <span className="highlight">clip.board</span>
        </h1>
      </div>

      {/* Rechte Sektion */}
      <div className="signup-right">
        <form className="signup-form" onSubmit={handleSignup}>
          {/* Name Felder */}
          <div className="name-fields">
            <input
              type="text"
              placeholder="First Name"
              value={first_name}
              onChange={(e) => setFirst_name(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Last Name"
              value={last_name}
              onChange={(e) => setLast_name(e.target.value)}
              required
            />
          </div>

          {/* Email-Feld */}
          <div className="input-group">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Passwort-Feld */}
          <div className="input-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Submit-Button */}
          <button type="submit" className="signup-button">Create Account</button>
        </form>

        {/* Nachricht nach dem Absenden */}
        {message && <p className="signup-message">{message}</p>}

        <p>
          Already have an account? <a href="/login" className="login-link">Log in</a>
        </p>
      </div>
    </div>
  );
}
export default SignupPage;

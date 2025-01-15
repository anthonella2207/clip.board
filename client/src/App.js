import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import MoviePage from "./pages/MoviePage";
import Sidebar from "./pages/Sidebar";
import { Navigate } from "react-router-dom";
import SignupPage from "./pages/SignupPage";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          {/* Rutas sin Sidebar */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            path="/*"
            element={
              <div className="layout">
                <Sidebar />
                <div className="main-content">
                  <Routes>
                    <Route path="/" element={<Navigate to="/home" />} />
                    <Route path="/home" element={<HomePage />} />
                    <Route path="/movie/:id" element={<MoviePage />} />
                  </Routes>
                </div>
              </div>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

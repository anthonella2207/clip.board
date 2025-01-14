import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import MoviePage from "./pages/MoviePage";
import Sidebar from "./pages/Sidebar";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <div className="layout">
          <Sidebar />
          <div className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/movie/:id" element={<MoviePage />} />
            </Routes>
          </div>
        </div>
      </Router>
    </div>
  );
}


export default App;

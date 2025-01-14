
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import MoviePage from "./pages/MoviePage";
import "./pages/HomePage.css"; // Ruta correcta al archivo CSS

function App() {
  return (
    <div className="App">
      {/* Rutas de la aplicación */}
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          {Array.from({ length: 20 }, (_, index) => (
            <Route
              key={index + 1}
              path={`/movie/${index + 1}`}
              element={<MoviePage movieId={index + 1} />}
            />
          ))}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
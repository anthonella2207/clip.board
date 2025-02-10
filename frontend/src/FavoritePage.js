import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./FavoritePage.css"; // Asegura que el nombre del archivo es correcto

const FavoritePage = () => {
  const [favoriteMovies, setFavoriteMovies] = useState([]);

  useEffect(() => {
    const storedFavorites = JSON.parse(localStorage.getItem("favoriteMovies")) || [];
    setFavoriteMovies(storedFavorites);
  }, []);

  const removeFromFavorites = (movieId) => {
    const updatedFavorites = favoriteMovies.filter(movie => movie.id !== movieId);
    setFavoriteMovies(updatedFavorites);
    localStorage.setItem("favoriteMovies", JSON.stringify(updatedFavorites));
  };

  return (
    <div className="favorites-container">
      <h1 className="favorites-title">Favorite Movies</h1>
      <Link to="/" className="back-link">⬅ Back to Home</Link>

      {favoriteMovies.length === 0 ? (
        <p className="no-favorites">No favorite movies yet.</p>
      ) : (
        <div className="movies-grid">
          {favoriteMovies.map((movie) => (
            <div key={movie.id} className="movie-card">
              <img
                src={`http://127.0.0.1:5000${movie.poster_path}`}
                alt={movie.title}
                className="movie-poster"
              />
              <h3 className="movie-title">{movie.title}</h3>
              <button className="remove-btn" onClick={() => removeFromFavorites(movie.id)}>
                ❌ Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FavoritePage;

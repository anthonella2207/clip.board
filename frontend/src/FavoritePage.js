import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { IoArrowBackOutline } from "react-icons/io5";
import "./FavoritePage.css"; // Asegura que el nombre del archivo es correcto

const FavoritePage = () => {
  const [favoriteMovies, setFavoriteMovies] = useState([]);

  useEffect(() => {
    const storedFavorites = JSON.parse(localStorage.getItem("favoriteMovies")) || [];
    setFavoriteMovies(storedFavorites);
  }, []);

  return (
    <div className="favorites-container">
      <Link to="/" className="back-link">⬅</Link>
      <h1 className="favorites-title">Book Later List</h1>

      {favoriteMovies.length === 0 ? (
        <p className="no-favorites">No favorite movies yet.</p>
      ) : (
        <div className="movies-grid">
          {favoriteMovies.map((movie) => (
            <div key={movie.id} className="movie-card">
              <img
                  src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                  alt={movie.title}
                  className="movie-poster"
                />
              <button className="book-now-btn">Book Now</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FavoritePage;

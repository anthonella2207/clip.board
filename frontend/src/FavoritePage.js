import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { IoArrowBackOutline } from "react-icons/io5";
import "./FavoritePage.css";

const FavoritePage = () => {
  const [favoriteMovies, setFavoriteMovies] = useState([]);

  useEffect(() => {
    const storedFavorites = JSON.parse(localStorage.getItem("favoriteMovies")) || [];
    setFavoriteMovies(storedFavorites);
  }, []);

  const removeFavorite = (id) => {
    const updatedFavorites = favoriteMovies.filter((movie) => movie.id !== id);
    setFavoriteMovies(updatedFavorites);
    localStorage.setItem("favoriteMovies", JSON.stringify(updatedFavorites));
  };

  return (
    <div className="favorites-container">
      <Link to="/" className="back-link">
        <IoArrowBackOutline />
      </Link>
      <h1 className="favorites-title">My Book Later List</h1>

      {favoriteMovies.length === 0 ? (
        <p className="no-favorites">No favorite movies yet.</p>
      ) : (
        <div className="movies-grid-2">
          {favoriteMovies.map((movie) => (
            <div key={movie.id} className="movie-card-2">
              <img
                src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                alt={movie.title}
                className="movie-poster-2"
              />
              <div className="movie-actions">
                <button className="remove-movie-btn" onClick={() => removeFavorite(movie.id)}>
                  Remove Movie
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FavoritePage;

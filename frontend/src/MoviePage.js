import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { FaHeart } from "react-icons/fa";
import "./MoviePage.css";

const API_KEY = "814254e9d1fb4859da3f4798b86b6f49";
const BASE_URL = "https://api.themoviedb.org/3";

const MoviePage = () => {
  const { id } = useParams(); // Obtiene el ID de la URL
  const [movie, setMovie] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await fetch(`${BASE_URL}/movie/${id}?api_key=${API_KEY}&language=en-US`);
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        const data = await response.json();
        console.log("Datos de la película:", data);
        setMovie(data);

        // Verificar si la película está en favoritos
        const storedFavorites = JSON.parse(localStorage.getItem("favoriteMovies")) || [];
        setIsFavorite(storedFavorites.some(fav => fav.id === data.id));
      } catch (error) {
        console.error("Error al obtener los detalles de la película:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  const toggleFavorite = () => {
    const storedFavorites = JSON.parse(localStorage.getItem("favoriteMovies")) || [];
    let updatedFavorites;

    if (isFavorite) {
      updatedFavorites = storedFavorites.filter(fav => fav.id !== movie.id);
    } else {
      updatedFavorites = [...storedFavorites, movie];
    }

    localStorage.setItem("favoriteMovies", JSON.stringify(updatedFavorites));
    setIsFavorite(!isFavorite);
  };

  if (isLoading) return <p>Loading movie details...</p>;
  if (!movie) return <p>Movie not found.</p>;

  return (
    <div className="movie-page">
      <div className="movie-container">
        <div className="movie-info">
          <div className="movie-title">
            {movie.title}
            <FaHeart
              className={`heart-icon ${isFavorite ? "favorite-active" : ""}`}
              onClick={toggleFavorite}
            />
          </div>
          <div className="movie-details">
            <p><strong>Genre:</strong> {movie.genres?.map(g => g.name).join(", ")}</p>
            <p><strong>Duration:</strong> {movie.runtime} minutes</p>
            <p><strong>Age Rating:</strong> {movie.adult ? "18+" : "All ages"}</p>
            <p><strong>Overview:</strong> {movie.overview}</p>
          </div>
        </div>
        <div className="movie-poster-container">
          <img
            src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
            alt={movie.title}
            className="movie-poster"
          />
        </div>
      </div>
    </div>
  );
};

export default MoviePage;

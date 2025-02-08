import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const MoviePage = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/movies/${id}`);
        const data = await response.json();
        setMovie(data);
      } catch (error) {
        console.error("Error fetching movie details:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  if (isLoading) return <p>Loading movie details...</p>;
  if (!movie) return <p>Movie not found</p>;

  return (
    <div className="movie-page">
      <h1>{movie.title}</h1>
      <img src={`http://127.0.0.1:5000${movie.poster_path}`} alt={movie.title} />
      <p><strong>Genre:</strong> {movie.genre}</p>
      <p><strong>Duration:</strong> {movie.runtime} minutes</p>
      <p><strong>Age Rating:</strong> {movie.age_rating}</p>
      <p><strong>Overview:</strong> {movie.overview}</p>
    </div>
  );
};

export default MoviePage;

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../Api";
import "./MoviePage.css";
import { Link } from "react-router-dom";

const MoviePage = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const movieResponse = await api.get(`/movie/${id}`, {
          params: { append_to_response: "credits" },
        });
        setMovie(movieResponse.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching movie:", error);
        setError(true);
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  if (loading) return <p>Loading movie...</p>;
  if (error) return <p>Error loading movie. Please try again later.</p>;

  const { title, overview, poster_path, release_date, vote_average, credits } = movie;
  const directors = credits.crew
    .filter((member) => member.job === "Director")
    .map((director) => director.name)
    .join(", ");
  const cast = credits.cast
    .slice(0, 5)
    .map((actor) => actor.name)
    .join(", ");

  return (
    <div className="movie-page-container">
      {/* Botón para volver */}
      <button className="back-button" onClick={() => window.history.back()}>
        ← Back
      </button>

      {/* Título */}
      <h1 className="movie-title">{title}</h1>

      {/* Contenido principal */}
      <div className="movie-main">
        {/* Descripción en rectángulo */}
        <div className="movie-details">
          <div className="transparent-box">
            <p className="movie-overview">{overview}</p>
          </div>
          {/* Información general en rectángulo */}
          <div className="transparent-box">
            <p><strong>Release Date:</strong> {release_date}</p>
            <p><strong>Rating:</strong> {vote_average}/10</p>
            <p><strong>Directors:</strong> {directors}</p>
            <p><strong>Main Cast:</strong> {cast}</p>
          </div>
        </div>

        {/* Poster y horarios */}
        <div className="poster-and-schedule">
          <img
            className="movie-poster"
            src={`https://image.tmdb.org/t/p/w500${poster_path}`}
            alt={title}
          />
          <div className="movie-schedule">
            <h2>Showtimes</h2>
            <Link to="/seats/1" className="schedule-item-link">
              <div className="schedule-item">
               3:00 PM - Kino 1
              </div>
            </Link>
            <Link to="/seats/2" className="schedule-item-link">
              <div className="schedule-item">
                6:00 PM - Kino 2
              </div>
            </Link>
            <Link to="/seats/3" className="schedule-item-link">
              <div className="schedule-item">
                9:00 PM - Kino 3
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
);
};

export default MoviePage;

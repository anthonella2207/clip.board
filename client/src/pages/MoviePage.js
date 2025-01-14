import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../Api";

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

  const { title, overview, poster_path, release_date, vote_average, credits } =
    movie;
  const directors = credits.crew
    .filter((member) => member.job === "Director")
    .map((director) => director.name)
    .join(", ");
  const cast = credits.cast
    .slice(0, 5)
    .map((actor) => actor.name)
    .join(", ");

  return (
    <div style={{ padding: "20px", color: "#fff" }}>
      <h1>{title}</h1>
      <p><strong>Overview:</strong> {overview}</p>
      <p><strong>Release Date:</strong> {release_date}</p>
      <p><strong>Rating:</strong> {vote_average}/10</p>
      <p><strong>Directors:</strong> {directors}</p>
      <p><strong>Main Cast:</strong> {cast}</p>
      <img
        src={`https://image.tmdb.org/t/p/w500${poster_path}`}
        alt={title}
        style={{ width: "300px", borderRadius: "10px" }}
      />
    </div>
  );
};

export default MoviePage;

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../Api"; // Configuración de tu cliente Axios
import "./HomePage.css";
import Filter from "./FilterPage"

const HomePage = () => {
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [actualMovies, setActualMovies] = useState([]);
  const [upcomingMovies, setUpcomingMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  //Filter states
  const [filters, setFilters] = useState({
    genre:"",
    min_duration:"",
    max_duration:"",
    age_rating:"",
  });

  const navigate = useNavigate();

  // Fetch movies from the API
  const fetchMovies = async () => {
    try {
      const [topRatedResponse, nowPlayingResponse, upcomingResponse] = await Promise.all([
        api.get("/movie/top_rated"), // Top Rated Movies
        api.get("/movie/now_playing"), // Currently Playing Movies
        api.get("/movie/upcoming"), // Upcoming Movies
      ]);

      const actualMoviesData = nowPlayingResponse.data.results.slice(0, 20); // First 20 movies
      const upcomingMoviesData = upcomingResponse.data.results
        .filter(
          (movie) => !actualMoviesData.some((actual) => actual.id === movie.id) // Exclude duplicates
        )
        .slice(0, 5); // First 5 unique movies

      setTopRatedMovies(topRatedResponse.data.results.slice(0, 3)); // Top Rated: 3 movies
      setActualMovies(actualMoviesData);
      setUpcomingMovies(upcomingMoviesData);
    } catch (error) {
      console.error("Error fetching data:", error.message);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, []);

   useEffect(() => {
        console.log("Current filters:", filters);

        const fetchFilteredMovies = async () => {
            try {
                const response = await api.get("http://localhost:5000/filters", { params: filters });
                setActualMovies(response.data.movies); // Aktualisiere die angezeigten Filme
            } catch (error) {
                console.error("Error fetching filtered movies:", error);
            }
        };

        if (filters.genre || filters.min_duration || filters.max_duration || filters.age_rating) {
            fetchFilteredMovies();
        }
    }, [filters]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  if (loading) {
    return <p>Loading movies...</p>;
  }

  if (error) {
    return <p>Error loading movies. Please try again later.</p>;
  }

  return (
    <div className="content">
      <Filter onFilter={handleFilterChange} />
      {/* Top Rated Section */}
      <div className="top-rated-section">
        <h1>Top Rated</h1>
        <div className="movies-grid">
          {topRatedMovies.map((movie) => (
            <div
              key={movie.id}
              className="movie-card"
              onClick={() => navigate(`/movie/${movie.id}`)}
            >
              <img
                src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                alt={movie.title}
                className="movie-poster"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Actual Section */}
      <div className="actual-section">
        <h1>Actual</h1>
        <div className="movies-grid">
          {actualMovies.map((movie) => (
            <div
              key={movie.id}
              className="movie-card"
              onClick={() => navigate(`/movie/${movie.id}`)}
            >
              <img
                src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                alt={movie.title}
                className="movie-poster"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Upcoming Section */}
      <div className="upcoming-section">
        <h1>Upcoming Movies</h1>
        <div className="movies-grid">
          {upcomingMovies.map((movie) => (
            <div
              key={movie.id}
              className="movie-card"
              onClick={() => navigate(`/movie/${movie.id}`)}
            >
              <img
                src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                alt={movie.title}
                className="movie-poster"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;

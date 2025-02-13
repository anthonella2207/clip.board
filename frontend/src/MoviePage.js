import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { FaRegClock, FaStar, FaStarHalfAlt, FaRegStar, FaClock } from "react-icons/fa";
import { IoMdClose } from "react-icons/io";
import { IoArrowBackOutline } from "react-icons/io5";
import "./MoviePage.css";

const API_KEY = "814254e9d1fb4859da3f4798b86b6f49";
const BASE_URL = "https://api.themoviedb.org/3";

const MoviePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [cast, setCast] = useState([]);
 const [showtimes, setShowtimes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isNowPlaying, setIsNowPlaying] = useState(false);
  const [isTopRated, setIsTopRated] = useState(false);
  const [isUpcoming, setIsUpcoming] = useState(false);
  const [favorites, setFavorites] = useState(
    JSON.parse(localStorage.getItem("favoriteMovies")) || []
  );

  const isFavorite = favorites.some(fav => fav.id === parseInt(id));

  useEffect(() => {
  const fetchMovie = async () => {
    try {
      const response = await fetch(`${BASE_URL}/movie/${id}?api_key=${API_KEY}&language=en-US`);
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const data = await response.json();
      setMovie(data);

      // Verificar si la película está en Now Playing
      const nowPlayingResponse = await fetch(`${BASE_URL}/movie/now_playing?api_key=${API_KEY}&language=en-US`);
      const nowPlayingData = await nowPlayingResponse.json();
      const isPlaying = nowPlayingData.results.some(m => m.id === data.id);
      setIsNowPlaying(isPlaying);

      // Si la película está en Now Playing, obtener los horarios desde Flask
      if (isPlaying) {
        const showtimesResponse = await fetch(`http://127.0.0.1:5000/api/showtimes/${data.id}`);
        const showtimesData = await showtimesResponse.json();
        setShowtimes(showtimesData);
        }

      // Verificar si la película está en Top Rated
      const topRatedResponse = await fetch(`${BASE_URL}/movie/top_rated?api_key=${API_KEY}&language=en-US`);
      const topRatedData = await topRatedResponse.json();
      setIsTopRated(topRatedData.results.some(m => m.id === data.id));

      // Verificar si la película está en Upcoming, pero solo si NO está en Now Playing
      if (!isPlaying) {
        const upcomingResponse = await fetch(`${BASE_URL}/movie/upcoming?api_key=${API_KEY}&language=en-US`);
        const upcomingData = await upcomingResponse.json();
        setIsUpcoming(upcomingData.results.some(m => m.id === data.id));
      } else {
        setIsUpcoming(false);
      }

    } catch (error) {
      console.error("Error fetching movie details:", error);
    } finally {
      setIsLoading(false);
    }
  };


    const fetchCast = async () => {
      try {
        const response = await fetch(`${BASE_URL}/movie/${id}/credits?api_key=${API_KEY}&language=en-US`);
        if (!response.ok) {
          throw new Error(`Error fetching cast: ${response.status}`);
        }
        const data = await response.json();
        setCast(data.cast.slice(0, 6));
      } catch (error) {
        console.error("Error fetching cast details:", error);
      }
    };

    fetchMovie();
    fetchCast();
  }, [id]);

  const toggleFavorite = () => {
    let updatedFavorites;
    if (isFavorite) {
      updatedFavorites = favorites.filter(fav => fav.id !== parseInt(id));
    } else {
      updatedFavorites = [...favorites, movie];
    }
    setFavorites(updatedFavorites);
    localStorage.setItem("favoriteMovies", JSON.stringify(updatedFavorites));
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating / 2);
    const halfStar = rating % 2 >= 1;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

    for (let i = 0; i < fullStars; i++) stars.push(<FaStar key={i} className="star" />);
    if (halfStar) stars.push(<FaStarHalfAlt key="half" className="star" />);
    for (let i = 0; i < emptyStars; i++) stars.push(<FaRegStar key={`empty-${i}`} className="star" />);

    return stars;
  };

  if (isLoading) return <p>Loading movie details...</p>;
  if (!movie) return <p>Movie not found.</p>;

  return (
    <div className="movie-page" style={{ backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.backdrop_path})` }}>
      <div className="overlay"></div>
      <button className="back-button" onClick={() => navigate("/")}>
        <IoArrowBackOutline />
      </button>

      <div className="movie-container">
        <div className="movie-poster-container">
          <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title} className="movie-poster-two" />
         {/* Mostrar "Watch Later" solo si la película está en Now Playing */}
          {isNowPlaying && (
            <button
              className={`watch-later ${isFavorite ? "watch-later-active" : ""}`}
              onClick={toggleFavorite}
              style={{ marginTop: "15px" }}
            >
              {isFavorite ? <IoMdClose /> : <FaRegClock />} {isFavorite ? "Remove from Book Later" : "Book Later"}
            </button>
          )}
        </div>

        <div className="movie-info-box">
          <p><strong>Genre:</strong> {movie.genres?.map((g) => g.name).join(", ")}</p>
          <p><strong>Duration:</strong> {movie.runtime} minutes</p>
          <p><strong>Age Rating:</strong> {movie.adult ? "18+" : "All ages"}</p>
          <p><strong>Overview:</strong> {movie.overview}</p>
          <p><strong>Cast:</strong> {cast.map(actor => actor.name).join(", ")}</p>
        </div>
      </div>

{/* Mostrar solo si es Now Playing */}
{isNowPlaying && (
  <div className="showtimes-box">
    <h3>Available Showtimes</h3>
    {showtimes.length > 0 ? (
      <div className="showtimes-list">
        {showtimes.map((show, index) => (
          <button
            key={index}
            className="showtime-button"
            onClick={() => navigate(`/seats/${show.id}`)}
            >
            🎥 {show.hall} - ⏰ {show.showtime}
          </button>
        ))}
      </div>
    ) : (
      <p>No showtimes available at the moment.</p>
    )}
  </div>
)}


      {/* Show just if it is Top Rated */}
      {isTopRated && (
        <div className="top-rated-box">
          <h3>Movie Rating: {movie.vote_average.toFixed(1)}</h3>
          <div className="stars">{renderStars(movie.vote_average)}</div>
          <p className="info-text">
            This movie is no longer playing in theaters, but it might return in the future due to its high popularity.
          </p>
        </div>
      )}

      {/* Show just if it is Upcoming */}
      {isUpcoming && (
        <div className="upcoming-box">
          <h3><FaClock className="upcoming-icon" /> Not now, but coming soon...</h3>
          <p className="info-text">
            This highly anticipated movie will be available soon. Stay tuned for its release date!
          </p>
        </div>
      )}
    </div>
  );
};

export default MoviePage;

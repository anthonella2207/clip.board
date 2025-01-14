import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import api from "../Api";
import { Swiper, SwiperSlide } from "swiper/react";
import { EffectCoverflow, Pagination, Navigation } from "swiper";
import "swiper/css";
import "swiper/css/effect-coverflow";
import "swiper/css/pagination";
import "swiper/css/navigation";
import "./HomePage.css";

const HomePage = () => {
  const [categories, setCategories] = useState([]);
  const [movies, setMovies] = useState([]);
  const [filteredMovies, setFilteredMovies] = useState([]);
  const [showAll, setShowAll] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const navigate = useNavigate();

  // Fetch movies and categories from the API
  const fetchMoviesAndCategories = async () => {
    try {
      const moviesResponse = await api.get("/movie/popular");
      const categoriesResponse = await api.get("/genre/movie/list");

      const uniqueMovies = Array.from(
        new Map(moviesResponse.data.results.map((movie) => [movie.id, movie]))
          .values()
      );

      const updatedCategories = [
        { id: 0, name: "All Movies" }, // Default option to show all movies
        ...categoriesResponse.data.genres, // Fetch genres from the API
      ];

      setCategories(updatedCategories);
      setMovies(uniqueMovies);
      setFilteredMovies(uniqueMovies);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  // Filter movies based on the selected category
  const handleFilter = (filterType, value) => {
    if (filterType === "category") {
      if (value === "All Movies") {
        setFilteredMovies(movies);
      } else {
        const filtered = movies.filter((movie) =>
          movie.genre_ids.includes(
            categories.find((cat) => cat.name === value)?.id
          )
        );
        setFilteredMovies(filtered);
      }
    }
  };

  useEffect(() => {
    fetchMoviesAndCategories();
  }, []);

  if (loading) {
    return <p>Loading movies...</p>;
  }

  if (error) {
    return <p>Error loading movies. Please try again later.</p>;
  }

  return (
    <div className="homepage">
      <Sidebar categories={categories} onFilter={handleFilter} />

      <div className="content">
        <header className="homepage-header">
          <div className="lamp-container">
            <img src="/lamp.png" alt="Lamp" className="lamp"/>
            <div className="light-effect"></div>
          </div>
          <h1>Clipboard</h1>
        </header>

        {!showAll ? (
          <Swiper
            modules={[EffectCoverflow, Pagination, Navigation]}
            effect="coverflow"
            grabCursor={true}
            centeredSlides={true}
            slidesPerView={5}
            loop={true}
            coverflowEffect={{
              rotate: 50,
              stretch: 0,
              depth: 100,
              modifier: 1,
            }}
            pagination={{
              clickable: true,
            }}
            navigation
            className="movie-carousel"
          >
            {filteredMovies.map((movie) => (
              <SwiperSlide
                key={movie.id}
                className="movie-slide"
                onClick={() => navigate(`/movie/${movie.id}`)}
              >
                <img
                  src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                  alt={movie.title}
                  className="movie-poster-carousel"
                />
              </SwiperSlide>
            ))}
          </Swiper>
        ) : (
          <div className="movies-grid">
            {filteredMovies.map((movie) => (
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
        )}
      </div>
    </div>
  );
};

export default HomePage;

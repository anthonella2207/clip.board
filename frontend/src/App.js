import React, { useEffect, useState } from "react";
import { FaHome, FaHeart, FaBook, FaSignInAlt } from "react-icons/fa";
import "./App.css";
import LoginPage from "./LoginPage";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import SignupPage from "./SignupPage";
import SeatSelection from "./SeatPage";


function App() {
  const [nowPlayingMovies, setNowPlayingMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [filteredTopRated, setFilteredTopRated] = useState([]);
  const [upcomingMovies, setUpcomingMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Filtros
  const [genre, setGenre] = useState("All");
  const [ageRating, setAgeRating] = useState("All");
  const [duration, setDuration] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  const menuItems = [
    { name: "Home", icon: <FaHome /> },
    { name: "Favorite", icon: <FaHeart /> },
    { name: "Bookings", icon: <FaBook /> },
  ];

  const bottomMenuItem = { name: "Login", icon: <FaSignInAlt /> };

  useEffect(() => {
  const fetchMovies = () => {
    const fetchMoviesByCategory = async (category, setMovies) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/movies/${category}`);
        const data = await response.json();
        setMovies(data);
      } catch (error) {
        console.error(`Error fetching ${category} movies:`, error);
      }
    };

    Promise.all([
      fetchMoviesByCategory("now_playing", setNowPlayingMovies),
      fetchMoviesByCategory("top_rated", setTopRatedMovies),
      fetchMoviesByCategory("upcoming", setUpcomingMovies),
    ]).then(() => setIsLoading(false));
  };

  // Comprobar última actualización
  const lastUpdated = localStorage.getItem("lastMovieUpdate");
  const now = new Date();
  const threeWeeks = 21 * 24 * 60 * 60 * 1000; // 21 días en milisegundos

  //if (!lastUpdated || now - new Date(lastUpdated) > threeWeeks) {
    fetchMovies();
    //localStorage.setItem("lastMovieUpdate", now.toISOString());
  //}

  // Actualizar cada 3 semanas automáticamente
  const interval = setInterval(() => {
    fetchMovies();
    localStorage.setItem("lastMovieUpdate", new Date().toISOString());
  }, threeWeeks);

  return () => clearInterval(interval);
}, []);

    // Manejar filtros
  useEffect(() => {
    const filtered = topRatedMovies.filter((movie) => {
      const matchesGenre = genre === "All" || movie.genre?.includes(genre);
      const matchesAgeRating = ageRating === "All" || movie.age_rating === ageRating;
      const matchesDuration =
        duration === "All" ||
        (duration === "<90" && movie.runtime < 90) ||
        (duration === "90-120" && movie.runtime >= 90 && movie.runtime <= 120) ||
        (duration === ">120" && movie.runtime > 120);
      const matchesSearch = movie.title.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesGenre && matchesAgeRating && matchesDuration && matchesSearch;
    });

    setFilteredTopRated(filtered);
  }, [genre, ageRating, duration, searchQuery, topRatedMovies]);


  return (
    <Router>
      <div className="App">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <h1>
              <span className="clip">clip</span>
              <span className="board">.board</span>
            </h1>
          </div>
          <ul className="menu-list">
            {menuItems.map((item, index) => (
              <li key={index} className="menu-item">
                {item.icon}
                <span>{item.name}</span>
              </li>
            ))}
          </ul>
          {/* Login at the bottom */}
          <div className="bottom-menu">
            <Link to="/login" className="menu-item">
              {bottomMenuItem.icon}
              <span>{bottomMenuItem.name}</span>
            </Link>
          </div>
        </div>

        {/* Main Content */}
        <div className="content">
          {/* Routes to handle login page */}
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/seats/:showId" element={<SeatSelection />} />
            {/* Default route that shows the home page */}
            <Route path="/" element={
              <div>
                {/* Filter Bar */}
                <div className="filter-bar">
                  <select value={genre} onChange={(e) => setGenre(e.target.value)}>
                    <option value="All">All Genres</option>
                    <option value="Action">Action</option>
                    <option value="Comedy">Comedy</option>
                    <option value="Drama">Drama</option>
                  </select>
                  <select value={ageRating} onChange={(e) => setAgeRating(e.target.value)}>
                    <option value="All">All Age Ratings</option>
                    <option value="G">G</option>
                    <option value="PG">PG</option>
                    <option value="PG-13">PG-13</option>
                    <option value="R">R</option>
                  </select>
                  <select value={duration} onChange={(e) => setDuration(e.target.value)}>
                    <option value="All">All Durations</option>
                    <option value="<90">Less than 90 minutes</option>
                    <option value="90-120">90-120 minutes</option>
                    <option value=">120">More than 120 minutes</option>
                  </select>
                  <input
                    type="text"
                    placeholder="Search by name"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>

                {/* Top Rated Section */}
                <h2 className="section-title">Our Top Rated Movies</h2>
                <div className="movies-grid">
                  {isLoading ? (
                    <p>Loading movies...</p>
                  ) : topRatedMovies.slice(0, 3).map((movie) => (
                    <div key={movie.id} className="movie-card">
                      <img
                        src={`http://127.0.0.1:5000${movie.poster_path}`}
                        alt={`${movie.title} poster`}
                        className="movie-poster"
                      />
                    </div>
                  ))}
                </div>

                {/* Now Playing Section */}
                <h2 className="section-title">Our Now Playing Movies</h2>
                <div className="movies-grid">
                  {isLoading ? (
                    <p>Loading movies...</p>
                  ) : nowPlayingMovies.slice(0, 20).map((movie) => (
                    <div key={movie.id} className="movie-card">
                      <img
                        src={`http://127.0.0.1:5000${movie.poster_path}`}
                        alt={`${movie.title} poster`}
                        className="movie-poster"
                      />
                    </div>
                  ))}
                </div>

                {/* Upcoming Section */}
                <h2 className="section-title">Our Upcoming Movies</h2>
                <div className="movies-grid">
                  {isLoading ? (
                    <p>Loading movies...</p>
                  ) : upcomingMovies.slice(0, 5).map((movie) => (
                    <div key={movie.id} className="movie-card">
                      <img
                        src={`http://127.0.0.1:5000${movie.poster_path}`}
                        alt={`${movie.title} poster`}
                        className="movie-poster"
                      />
                    </div>
                  ))}
                </div>
              </div>
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

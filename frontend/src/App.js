import React, { useEffect, useState, useContext } from "react";
import { FaClock, FaHome, FaBook, FaSignInAlt } from "react-icons/fa";
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
import "./App.css";
import LoginPage from "./LoginPage";
import SignupPage from "./SignupPage";
import SeatSelection from "./SeatPage";
import MoviePage from "./MoviePage";
import FavoritePage from "./FavoritePage";
import MovieFilter from "./filter";
import BookingConfirmation from "./BookingConfirmation";
import { AuthProvider } from "./AuthContext";
import { AuthContext } from "./AuthContext";
import ProfilePage from "./ProfilePage";

function AppContent() {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();

  useEffect(() => {
    console.log("🔄 App hat sich aktualisiert. User: ", user);
  }, [user]);

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
  const [voteAverage, setVoteAverage] = useState("All");

  const menuItems = [
    { name: "Home", icon: <FaHome />, link: "/" },
    { name: "Book Later", icon: <FaClock />, link: "/book-later" },
    { name: "Bookings", icon: <FaBook />, link: "/bookings" },
  ];

  if (user) {
    menuItems.push({ name: "Profile", icon: <FaSignInAlt />, link: "/profile" });
  }

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

    const lastUpdated = localStorage.getItem("lastMovieUpdate");
    const now = new Date();
    const threeWeeks = 21 * 24 * 60 * 60 * 1000;

    fetchMovies();

    const interval = setInterval(() => {
      fetchMovies();
      localStorage.setItem("lastMovieUpdate", new Date().toISOString());
    }, threeWeeks);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchFilteredMovies = async () => {
      try {
        const queryParams = new URLSearchParams({
          genres: genre !== "All" ? genre : "",
          duration: duration !== "All" ? duration : "",
          vote_average: voteAverage !== "All" ? voteAverage : "",
          keywords: searchQuery !== "" ? searchQuery : "",
        });

        const response = await fetch(`http://127.0.0.1:5000/api/movies/now_playing?${queryParams}`);
        const data = await response.json();
        console.log("DEBUG: API response:", data);

        if (data.success && Array.isArray(data.movies)) {
          setNowPlayingMovies(data.movies);
        } else {
          setNowPlayingMovies([]);
        }
      } catch (error) {
        console.error("Error fetching filtered now-playing movies:", error);
        setNowPlayingMovies([]);
        console.log(nowPlayingMovies);
      }
    };

    fetchFilteredMovies();
  }, [genre, duration, voteAverage, searchQuery]);

  return (
    <div className="App">
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>
            <span className="clip">clip</span>
            <span className="board">.board</span>
          </h1>
        </div>
        <ul className="menu-list">
          {menuItems.map((item, index) => {
            const isActive = location.pathname === item.link;
            return (
              <Link
                to={item.link}
                className={`menu-link ${isActive ? "active-menu" : ""}`}
                key={index}
              >
                {item.icon}
                <span>{item.name}</span>
              </Link>
            );
          })}
        </ul>

        <div className="bottom-menu">
          {user ? (
            <button onClick={logout} className="log-button">
              <FaSignInAlt />
              <span>Logout</span>
            </button>
          ) : (
            <Link to="/login" className="login-button">
              <FaSignInAlt />
              <span>Login</span>
            </Link>
          )}
        </div>
      </div>

      <div className="content">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/seats/:showId" element={<SeatSelection />} />
          <Route path="/movie/:id" element={<MoviePage />} />
          <Route path="/book-later" element={<FavoritePage />} />
          <Route path="/booking-confirmation" element={<BookingConfirmation />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/" element={
            <div>
              <MovieFilter onFilterChange={({ genre, duration, voteAverage, searchQuery }) => {
                setGenre(genre);
                setDuration(duration);
                setVoteAverage(voteAverage);
                setSearchQuery(searchQuery);
              }} />

              <h2 className="section-title">Our Top Rated Movies</h2>
              <div className="movies-grid">
                {isLoading ? (
                  <p>Loading movies...</p>
                ) : topRatedMovies.slice(0, 3).map((movie) => (
                  <div key={movie.id} className="movie-card">
                    <Link to={`/movie/${movie.id}`}>
                      <img src={`http://127.0.0.1:5000${movie.poster_path}`} alt={`${movie.title} poster`}
                        className="movie-poster" />
                    </Link>
                  </div>
                ))}
              </div>

              <h2 className="section-title">Our Now Playing Movies</h2>
              <div className="movies-grid">
                {isLoading ? (
                  <p>Loading movies...</p>
                ) : (Array.isArray(nowPlayingMovies) ? nowPlayingMovies.slice(0, 20).map((movie) => (
                  <div key={movie.id} className="movie-card">
                    <Link to={`/movie/${movie.id}`}>
                      <img
                        src={`http://127.0.0.1:5000${movie.poster_path}`}
                        alt={`${movie.title} poster`}
                        className="movie-poster"
                      />
                    </Link>
                  </div>
                )) : <p>No movies found.</p>)}
              </div>

              <h2 className="section-title">Our Upcoming Movies</h2>
              <div className="movies-grid">
                {isLoading ? (
                  <p>Loading movies...</p>
                ) : upcomingMovies.slice(0, 5).map((movie) => (
                  <div key={movie.id} className="movie-card">
                    <Link to={`/movie/${movie.id}`}>
                      <img src={`http://127.0.0.1:5000${movie.poster_path}`} alt={`${movie.title} poster`}
                        className="movie-poster" />
                    </Link>
                  </div>
                ))}
              </div>
            </div>
          } />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default function RootApp() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}
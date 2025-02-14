import React, { useEffect, useState, useContext } from "react";
import { FaClock, FaHome, FaBook, FaSignInAlt, FaShoppingCart } from "react-icons/fa";
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
import AdminShowSelection from "./AdminShowSelection";
import { FaStairs } from "react-icons/fa6";
import StatisticsPage from "./Statistics";
import AdminLogs from "./AdminLogs";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation(); // Get the current path

  useEffect(() => {
    console.log("🔄 App hat sich aktualisiert. User: ", user);
  }, [user]);

  const [nowPlayingMovies, setNowPlayingMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
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
    if (user.role === "Admin") {
      menuItems.push(
        { name: "Reservations", icon: <FaShoppingCart />, link: "/reservations" },
        { name: "Logs", icon: <FaBook />, link: "/logs" },
        { name: "Profile", icon: <FaSignInAlt />, link: "/profile" },
        { name: "Stats", icon: <FaStairs />, link: "/statistics" }
      );
    } else {
      menuItems.push({ name: "Profile", icon: <FaSignInAlt />, link: "/profile" });
    }
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

    fetchMovies();

    const interval = setInterval(() => {
      fetchMovies();
      localStorage.setItem("lastMovieUpdate", new Date().toISOString());
    }, 21 * 24 * 60 * 60 * 1000); // 21 days in milliseconds

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
      }
    };

    fetchFilteredMovies();
  }, [genre, duration, voteAverage, searchQuery]);

  return (
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
          {menuItems.map((item, index) => {
            const isActive = location.pathname === item.link; // Check if it's the current page
            return (
              <Link
                to={item.link}
                className={`menu-link ${isActive ? "active-menu" : ""}`} // Apply the class if active
                key={index}
              >
                {item.icon}
                <span>{item.name}</span>
              </Link>
            );
          })}
        </ul>

        {/* Login at the bottom */}
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

      {/* Main Content */}
      <div className="content">
        {/* Routes to handle login page */}
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/movie/:id" element={<MoviePage />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/seats/:showId" element={<SeatSelection />} />
            <Route path="/book-later" element={<FavoritePage />} />
            <Route path="/booking-confirmation" element={<BookingConfirmation />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/reservations" element={<AdminShowSelection />} />
            <Route path="/reservations/:showId" element={<SeatSelection />} />
            <Route path="/statistics" element={<StatisticsPage />} />
            <Route path="/logs" element={<AdminLogs />} />
          </Route>

          {/* Default route that shows the home page */}
          <Route
            path="/"
            element={
              <div>
                {/* Filter Bar */}
                <MovieFilter
                  onFilterChange={({ genre, duration, voteAverage, searchQuery }) => {
                    setGenre(genre);
                    setDuration(duration);
                    setVoteAverage(voteAverage);
                    setSearchQuery(searchQuery);
                  }}
                />

                {/* Top Rated Section */}
                <h2 className="section-title">Our Top Rated Movies</h2>
                <div className="movies-grid">
                  {isLoading ? (
                    <p>Loading movies...</p>
                  ) : (
                    topRatedMovies.slice(0, 3).map((movie) => (
                      <div key={movie.id} className="movie-card">
                        <Link to={`/movie/${movie.id}`}>
                          <img
                            src={`http://127.0.0.1:5000${movie.poster_path}`}
                            alt={`${movie.title} poster`}
                            className="movie-poster"
                          />
                        </Link>
                      </div>
                    ))
                  )}
                </div>

                {/* Now Playing Section */}
                <h2 className="section-title">Our Now Playing Movies</h2>
                <div className="movies-grid">
                  {isLoading ? (
                    <p>Loading movies...</p>
                  ) : Array.isArray(nowPlayingMovies) ? (
                    nowPlayingMovies.slice(0, 20).map((movie) => (
                      <div key={movie.id} className="movie-card">
                        <Link to={`/movie/${movie.id}`}>
                          <img
                            src={`http://127.0.0.1:5000${movie.poster_path}`}
                            alt={`${movie.title} poster`}
                            className="movie-poster"
                          />
                        </Link>
                      </div>
                    ))
                  ) : (
                    <p>No movies found.</p>
                  )}
                </div>

                {/* Upcoming Section */}
                <h2 className="section-title">Our Upcoming Movies</h2>
                <div className="movies-grid">
                  {isLoading ? (
                    <p>Loading movies...</p>
                  ) : (
                    upcomingMovies.slice(0, 5).map((movie) => (
                      <div key={movie.id} className="movie-card">
                        <Link to={`/movie/${movie.id}`}>
                          <img
                            src={`http://127.0.0.1:5000${movie.poster_path}`}
                            alt={`${movie.title} poster`}
                            className="movie-poster"
                          />
                        </Link>
                      </div>
                    ))
                  )}
                </div>
              </div>
            }
          />
        </Routes>
      </div>
    </div>
  );
}

export default function RootApp() {
  return (
    <Router>
      <AuthProvider>
        <App />
      </AuthProvider>
    </Router>
  );
}
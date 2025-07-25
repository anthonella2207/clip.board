import React, { useEffect, useState, useContext } from "react";
import { FaClock, FaHome, FaSignInAlt } from "react-icons/fa";
import { MdBookmarkAdded } from "react-icons/md";
import { GiHistogram } from "react-icons/gi";
import { CiLogin } from "react-icons/ci";
import { GrContactInfo } from "react-icons/gr";
import { TbBookmarkQuestion } from "react-icons/tb";
import { CgProfile } from "react-icons/cg";
import { BiSupport } from "react-icons/bi"; // Import the support icon
import "./App.css";
import LoginPage from "./LoginPage";
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
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
import StatisticsPage from "./Statistics";
import AdminLogs from "./AdminLogs";
import ProtectedRoute from "./ProtectedRoute";
import Loader from "./Loader"; // Import the Loader component
import BookingPage from "./BookingPage";
import SupportPage from "./SupportPage"; // Import the SupportPage

function App() {
  const { user, logout } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);
  const location = useLocation();

  //logs when user state changes
  useEffect(() => {
    console.log("App hat sich aktualisiert. User: ", user);
  }, [user]);

  //simulates loading animation
  useEffect(() => {
    if (loading) {
      const timer = setTimeout(() => setLoading(false), 1000); // Simulate loading for 1 second
      return () => clearTimeout(timer);
    }
  }, [loading]);

  const handleLinkClick = () => {
    setLoading(true);
  };

  const handleLogout = () => {
    logout();
  };

  //state for movie categories
  const [nowPlayingMovies, setNowPlayingMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [filteredTopRated, setFilteredTopRated] = useState([]);
  const [upcomingMovies, setUpcomingMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // states for filters
  const [genre, setGenre] = useState("All");
  const [ageRating, setAgeRating] = useState("All");
  const [duration, setDuration] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [voteAverage, setVoteAverage] = useState("All");

  // Menu items for regular users
  const regularMenuItems = [
    { name: "Home", icon: <FaHome />, link: "/" },
    { name: "Book Later", icon: <FaClock />, link: "/book-later" },
    { name: "Bookings", icon: <MdBookmarkAdded />, link: "/bookings" },
    { name: "Support", icon: <BiSupport />, link: "/support" } // Add SupportPage link
  ];

  // Admin-specific menu items
  const adminMenuItems = [
    { name: "Availability", icon: <TbBookmarkQuestion />, link: "/reservations" },
    { name: "User Activity", icon: <GrContactInfo />, link: "/logs" },
    { name: "Statistics", icon: <GiHistogram />, link: "/statistics" }
  ];

  const bottomMenuItem = { name: "Login", icon: <FaSignInAlt /> };

  // Fetch movies from API
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

      // Fetch all categories simultaneously
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

  // Fetch filtered movies based on user selections
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
          setNowPlayingMovies([]); // Set empty array if no valid response
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
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>
            <span className="clip">clip</span>
            <span className="board">.board</span>
          </h1>
        </div>
        <ul className="menu-list">
          {regularMenuItems.map((item, index) => {
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

        {user && user.role === "Admin" && (
          <div className="admin-container">
            <h3>Admin Options</h3>
            <ul className="menu-list">
              {adminMenuItems.map((item, index) => {
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
          </div>
        )}
        {/* Login at the bottom */}
        <div className="bottom-menu">
          {user ? (
            <div className="profile-menu">
              <Link to="/profile" className="menu-link">
                <CgProfile size={28} /> {/* Only the icon without text */}
              </Link>
            </div>
          ) : (
            <Link to="/login" className="login-button">
              <CiLogin />
              <span>Login</span>
            </Link>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="content">
        {loading ? (
          <Loader />
        ) : (
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
              <Route path="/bookings" element={<BookingPage userId={user?.id} />} />
            </Route>

            <Route path="/support" element={<SupportPage />} /> {/* Add SupportPage route */}

            <Route
              path="/"
              element={
                <div>
                  <div className="filter-container">
                    <MovieFilter
                      onFilterChange={({ genre, duration, voteAverage, searchQuery }) => {
                        setGenre(genre);
                        setDuration(duration);
                        setVoteAverage(voteAverage);
                        setSearchQuery(searchQuery);
                      }}
                    />
                  </div>

                  <h2 className="section-title">Our Top Rated Movies</h2>
                  <div className="movies-grid">
                    {isLoading ? (
                      <Loader />
                    ) : (
                      topRatedMovies.slice(0, 3).map((movie) => (
                        <div key={movie.id} className="movie-card">
                          <Link to={`/movie/${movie.id}`} onClick={handleLinkClick}>
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

                  <h2 className="section-title">Our Now Playing Movies</h2>
                  <div className="movies-grid">
                    {isLoading ? (
                      <Loader />
                    ) : Array.isArray(nowPlayingMovies) ? (
                      nowPlayingMovies.slice(0, 20).map((movie) => (
                        <div key={movie.id} className="movie-card">
                          <Link to={`/movie/${movie.id}`} onClick={handleLinkClick}>
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

                  <h2 className="section-title">Our Upcoming Movies</h2>
                  <div className="movies-grid">
                    {isLoading ? (
                      <Loader />
                    ) : (
                      upcomingMovies.slice(0, 5).map((movie) => (
                        <div key={movie.id} className="movie-card">
                          <Link to={`/movie/${movie.id}`} onClick={handleLinkClick}>
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
        )}
      </div>
    </div>
  );
}
// Wrap App with Router and AuthProvider
export default function RootApp() {
  return (
    <Router>
      <AuthProvider>
        <App />
      </AuthProvider>
    </Router>
  );
}
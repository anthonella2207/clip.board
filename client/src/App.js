import React, { useEffect, useState } from "react";
import api from "./Api"; // Importa tu archivo Api.js
import "./App.css";

function App() {
  const [movies, setMovies] = useState([]); // Estado para las películas
  const [loading, setLoading] = useState(true); // Estado para mostrar el indicador de carga
  const [error, setError] = useState(null); // Estado para manejar errores

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await api.get("/movie/popular"); // Llamada a la API
        setMovies(response.data.results); // Guarda las películas en el estado
      } catch (err) {
        setError("Error al cargar las películas. Intenta más tarde.");
      } finally {
        setLoading(false); // Detiene el estado de carga
      }
    };

    fetchMovies(); // Llama a la función
  }, []);

  return (
    <div className="background">
      <h1 className="title">CLIPBOARD</h1>
      <p className="subtitle">The Magic of the Cinema</p>

      {loading && <p>Cargando películas...</p>}
      {error && <p>{error}</p>}

      <div className="movies">
        {movies.map((movie) => (
          <div key={movie.id} className="movie">
            <img
              src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
              alt={movie.title}
            />
            <h3>{movie.title}</h3>
            <p>Rating: {movie.vote_average}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

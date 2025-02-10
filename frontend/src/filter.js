import React, { useEffect, useState } from "react";

const MovieFilter = ({ onFilterChange }) => {
  const [genres, setGenres] = useState(["All"]);
  const [selectedGenre, setSelectedGenre] = useState("All");
  const [selectedDuration, setSelectedDuration] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/genres");
        const data = await response.json();
        if (data.genres) {
          setGenres(["All", ...data.genres]);
        }
      } catch (error) {
        console.error("Error fetching genres:", error);
      }
    };

    fetchGenres();
  }, []);


  // Wird aufgerufen, wenn ein Filter geändert wird
  useEffect(() => {
    onFilterChange({ genre: selectedGenre, duration: selectedDuration, searchQuery });
  }, [selectedGenre, selectedDuration, searchQuery]);

  return (
    <div className="filter-bar">
      <select value={selectedGenre} onChange={(e) => setSelectedGenre(e.target.value)}>
        {genres.map((g, index) => (
          <option key={index} value={g}>{g}</option>
        ))}
      </select>

      <select value={selectedDuration} onChange={(e) => setSelectedDuration(e.target.value)}>
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
  );
};

export default MovieFilter;

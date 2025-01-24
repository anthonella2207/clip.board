import React, {useEffect, useState} from 'react';

function Filter({ onFilter }) {
    const[genre, setGenre] = useState('');
    const[min_duration, setMinDuration] = useState('');
    const[max_duration, setMaxDuration] = useState('');
    const[age_rating, setAgeRating] = useState('');
    const[genres, setGenres] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/filters/available-genres')
    .then(response => {
        if (!response.ok) {
            // Wenn der Statuscode nicht 2xx ist (z. B. 404 oder 500)
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();  // Parse die Antwort als JSON
    })
    .then(data => {
        console.log(data);  // Zeige die Antwort an, um sicherzustellen, dass es die Genres sind
        setGenres(data.genres || []);
    })
    .catch(error => {
        console.error("Error occurred while retrieving genres", error);
        // Zeige eine Fehlermeldung an
    });
    }, []);

    const handleSubmit = () => {
        const filters = {
            genre: genre,
            min_duration: min_duration,
            max_duration: max_duration,
            age_rating: age_rating,
        };
        onFilter(filters);
    };

    return (
        <div id="filters">
            <select
                id="genreFilter"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}>
                <option value="">Choose a genre</option>
                {genres.map((genre, index) => (
                    <option key={index} value={genre}>
                        {genre}
                    </option>
                ))}
            </select>

            <input
                type="number"
                id="minDuration"
                value={min_duration}
                onChange={(e) => setMinDuration(e.target.value)}
                placeholder="Min. Dauer (Minuten)"
            />
            <input
                type="number"
                id="maxDuration"
                value={max_duration}
                onChange={(e) => setMaxDuration(e.target.value)}
                placeholder="Max. Dauer (Minuten)"
            />
            <select
                id="ageRatingFilter"
                value={age_rating}
                onChange={(e) => setAgeRating(e.target.value)}>
                <option value="">Choose age rating</option>
                <option value="PG">PG</option>
                <option value="R">R</option>
            </select>

            <button onClick={handleSubmit}>filter</button>

        </div>
    );
}

export default Filter;
import React, {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import "./AdminShowSelection.css"

function AdminShowSelection(){
    //state to save available shows
    const[shows, setShows] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        //called at first render, to load movies
        const fetchShows = async () => {
            try{
                //request to backend to get available shows
                const response = await fetch(`http://127.0.0.1:5000/api/available_shows`);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                //convert answer to json
                const data = await response.json();
                console.log("Fetched Shows:", data);

                setShows(data.available_shows || []);
            }
            catch(error){
                console.error("Error fetching shows:", error);
                setShows([]);
            }
        };
        fetchShows();
    }, []);

    const handleShowSelection = (showId) => {
        navigate(`/reservations/${showId}`);
    };

    return (
        <div className="reservations-page">
            <h2>Select a Show</h2>
            {shows.length === 0 ? (
                <p>Loading available shows...</p>
            ) : (
                <ul className="reservations-container">
                    {shows.map((show) => (
                        <li key={show.show_id}>
                            <button className="reservations-actions" onClick={() => handleShowSelection(show.show_id)}>
                                {show.title}
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default AdminShowSelection;
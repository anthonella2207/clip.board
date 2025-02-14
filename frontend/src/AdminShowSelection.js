import React, {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import "./AdminShowSelection.css"

function AdminShowSelection(){
    const[showIds, setShowIds] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchShows = async () => {
            try{
                const response = await fetch(`http://127.0.0.1:5000/api/available_shows`);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log("Fetched Shows:", data);

                setShowIds(data.available_shows || []);
            }
            catch(error){
                console.error("Error fetching shows:", error);
                setShowIds([]);
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
            {showIds.length === 0 ? (
                <p>Loading available shows...</p>
            ) : (
                <ul className="reservations-container">
                    {showIds.map((showId) => (
                        <li key={showId}>
                            <button className="reservations-actions" onClick={() => handleShowSelection(showId)}>
                                Show ID: {showId}
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default AdminShowSelection;
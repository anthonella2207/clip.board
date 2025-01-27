import React, {useEffect, useState} from "react";
import './SeatPage.css'
import {useParams} from "react-router-dom";

const SeatPage = () => {
    const {hallId} = useParams()
    const [seats, setSeats] = useState([])
    const [selectedSeats, setSelectedSeats] = useState([])

    useEffect(() => {
    fetch(`http://localhost:5000/api/seats?hall_id=${hallId}`)
        .then((response) => response.json())
        .then((data) => {
            console.log("Sitzplan-Daten:", data); // Hier wird die Antwort in der Konsole ausgegeben
            setSeats(data);  // Setzt die Daten in den State
        })
        .catch((error) => console.error('Error occurred:', error));
}, [hallId]);

    const toggleSeatSelection = (seatId) => {
        setSelectedSeats((prevSelectedSeats) => {
            if(prevSelectedSeats.includes(seatId)){
                return prevSelectedSeats.filter((id) => id !== seatId);
            }
            else{
                return [...prevSelectedSeats, seatId];
            }
        });
    };


  return (
      <div className="seat-page">
          <div className="seat-title">Sitzplan für Saal {hallId}</div>
          <div className="seat-grid">
              {seats.map((seat) => (
                  <div
                      key={seat.id}
                      className={`seat ${seat.isBooked ? 'seat-booked' : ''} ${selectedSeats.includes(seat.id) ? 'seat-selected' : ''}`}
                      onClick={() => {
                          if (!seat.isBooked) toggleSeatSelection(seat.id);
                      }}
                  >
                      {seat.row_number}-{seat.seat_number}
                  </div>
              ))}
          </div>
          <div className="summary">
              <h2>Ausgewählte Sitze:</h2>
              <p>{selectedSeats.join(', ') || 'Keine Sitze ausgewählt'}</p>
              <button className="booking-button">
                  Book now!
              </button>
          </div>
      </div>
  );
};

export default SeatPage;
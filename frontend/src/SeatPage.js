import React, {use, useEffect, useState, useRef} from "react";
import './SeatPage.css'
import {useParams} from "react-router-dom";

const fetchSeats = async (showId) => {
    try {
        console.log(`Fetching seats for showId: ${showId}`);
        const response = await fetch(`http://localhost:5000/api/seats/${showId}`);
        console.log(`API Response Status: ${response.status}`);
        if (!response.ok) {
            throw new Error("Error fetching the seats");
        }
        const data = await response.json();
        console.log(`API Data Received:`, data);
        return data.seats || [];
    } catch (error) {
        console.error(error);
        return [];
    }
};

export default function SeatSelection() {
    const { showId } = useParams();
    const[seats, setSeats] = useState([]);
    const[selectedSeats, setSelectedSeats] = useState([]);
    const[totalPrice, setTotalPrice] = useState(0);

    const hasFetched = useRef(false);

    useEffect(() => {
    if (!hasFetched.current) {
        hasFetched.current = true;
        fetchSeats(showId).then((data) => {
            console.log("Seats received:", data);
            setSeats(data);
        });
    }
}, [showId]);

useEffect(() => {
    const newTotalPrice = selectedSeats.reduce((acc, seatId) => {
        const seat = seats.find(s => s.id === seatId);
        return acc + (seat ? Number(seat.price) : 0);
    }, 0);

    console.log("Neuer Gesamtpreis berechnet:", newTotalPrice);
    setTotalPrice(newTotalPrice);
}, [selectedSeats, seats]);

    const toggleSeatSelection = (seatId, seatPrice) => {
        const price = Number(seatPrice) || 0;

        console.log("Toggle für Sitz:", seatId, "| Preis erhalten:", seatPrice, "| Typ:", typeof seatPrice, "| Konvertiert:", price);
        console.log("Vorheriger Gesamtpreis:", totalPrice);

        setSelectedSeats((prevSelectedSeats) => {
            if(prevSelectedSeats.includes(seatId)){
                setTotalPrice(prevTotal => prevTotal - price);
                return prevSelectedSeats.filter((id) => id !== seatId);
            }
            else{
                setTotalPrice(prevTotal => prevTotal + price);
                return [...prevSelectedSeats, seatId];
            }
        });
    };

    return (
        <div className="seat-page">
            <h2 className="seat-title">Seat selection</h2>
            <div className="seat-grid">
                {seats.length > 0 ?(
                    seats.map((seat) => (
                        console.log("Seat price check:", seat.price),
                        <div
                            key={seat.id}
                            className={`seat ${seat.isbooked ? "seat-booked": ""}
                            ${selectedSeats.includes(seat.id) ? "seat-selected": ""}`}
                            onClick={() => !seat.isbooked && toggleSeatSelection(seat.id, Number(seat.price) || 0)}>
                            {seat.row_number}-{seat.seat_number}
                        </div>
                    ))
                ) : (
                    <p>Loading seats...</p>
                )}
            </div>
            <div className="summary">
                {selectedSeats.length > 0 ? (
                    <>
                        <p>Selected Seats: {selectedSeats.join(", ")}</p>
                        <p><strong>Total price: €{totalPrice.toFixed(2)}</strong></p>
                    </>

                ) : (
                    <p>No seats selected</p>
                )}
            </div>
            <button
                className="booking-button"
                disabled={selectedSeats.length === 0}
                onClick={() => alert(`You sure you want to proceed booking seats: ${selectedSeats.join(", ")}`)} >
                Book Now!
            </button>
        </div>
    );
}
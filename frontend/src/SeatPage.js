import React, { useEffect, useState, useRef, useContext } from "react";
import { MdEventSeat } from "react-icons/md"; // Importar icono de asiento
import './SeatPage.css';
import { useParams, useNavigate } from "react-router-dom";
import reserveSeats from "./Reservation";
import { AuthContext } from "./AuthContext";

const fetchSeats = async (showId) => {
    try {
        const response = await fetch(`http://localhost:5000/api/seats/${showId}`);
        if (!response.ok) {
            throw new Error("Error fetching the seats");
        }
        const data = await response.json();
        return data.seats || [];
    } catch (error) {
        console.error(error);
        return [];
    }
};

export default function SeatSelection() {
    const { showId } = useParams();
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();
    const [seats, setSeats] = useState([]);
    const [selectedSeats, setSelectedSeats] = useState([]);
    const [totalPrice, setTotalPrice] = useState(0);
    const [buttonActive, setButtonActive] = useState(false); // Estado para cambiar el color del botón

    const hasFetched = useRef(false);

    useEffect(() => {
        if (!hasFetched.current) {
            hasFetched.current = true;
            fetchSeats(showId).then((data) => {
                setSeats(data);
            });
        }
    }, [showId]);

    useEffect(() => {
        const newTotalPrice = selectedSeats.reduce((acc, seatId) => {
            const seat = seats.find(s => s.id === seatId);
            return acc + (seat ? Number(seat.price) : 0);
        }, 0);
        setTotalPrice(newTotalPrice);

        // Cambiar estado del botón dependiendo de la selección de asientos
        setButtonActive(selectedSeats.length > 0);
    }, [selectedSeats, seats]);

    const toggleSeatSelection = (seatId, seatPrice) => {
        const price = Number(seatPrice) || 0;

        setSelectedSeats((prevSelectedSeats) => {
            if (prevSelectedSeats.includes(seatId)) {
                setTotalPrice(prevTotal => prevTotal - price);
                return prevSelectedSeats.filter((id) => id !== seatId);
            } else {
                setTotalPrice(prevTotal => prevTotal + price);
                return [...prevSelectedSeats, seatId];
            }
        });
    };

    const handleReservation = async () => {
        if (!user) {
            alert("You need to log in first!");
            navigate("/login");
            return;
        }

        if (selectedSeats.length === 0) {
            alert("Please select a seat.");
            return;
        }

        const confirmBooking = window.confirm("Are you sure, you want to continue?");
        if (!confirmBooking) {
            return;
        }

        const result = await reserveSeats(user.id, showId, selectedSeats);

        if (result.success) {
            navigate("/booking-confirmation", {
                state: {
                    reservationId: result.reservationId,
                    totalPrice: totalPrice,
                },
            });
        } else {
            alert(`Error reserving: ${result.message}`);
        }
    };

    return (
        <div className="seat-page">
            <h2 className="seat-title">Please select your seat </h2>
            <div className="screen"></div>
            <div className="seat-container">
                <div className="row-numbers">
                    {Array.from({ length: 10 }, (_, i) => (
                        <div key={i + 1} className="row-number">{i + 1}</div>
                    ))}
                </div>
                <div className="seat-grid">
                    {seats.length > 0 ? (
                        seats.map((seat) => (
                            <button
                                key={seat.id}
                                className={`seat 
                                    ${seat.isbooked ? "seat-booked" : "seat-free"}
                                    ${selectedSeats.includes(seat.id) ? "seat-selected" : ""}`}
                                onClick={() => !seat.isbooked && toggleSeatSelection(seat.id, Number(seat.price) || 0)}
                            >
                                <div className="seat-tooltip">ROW {seat.row_number} SEAT {seat.seat_number}</div>
                                <MdEventSeat size={20} />
                            </button>
                        ))
                    ) : (
                        <p>Loading seats...</p>
                    )}
                </div>
            </div>
            <div className="summary">
                {selectedSeats.length > 0 ? (
                    <>
                        <p>Selected Seats: {selectedSeats.join(", ")}</p>
                        <p><strong>Total Price: €{totalPrice.toFixed(2)}</strong></p>
                    </>
                ) : (
                    <p>No seats selected</p>
                )}
            </div>
            <button
                className={`booking-button ${buttonActive ? "active" : ""}`}
                disabled={selectedSeats.length === 0}
                onClick={handleReservation}
            >
                Book Now!
            </button>
        </div>
    );
}

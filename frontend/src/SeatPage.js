import React, {useEffect, useState, useRef, useContext, useCallback} from "react";
import './SeatPage.css'
import { MdEventSeat } from "react-icons/md";
import { useParams, useNavigate } from "react-router-dom";
import reserveSeats from "./Reservation";
import {AuthContext} from "./AuthContext";
import {Pie} from "react-chartjs-2";
import { Chart, ArcElement, Tooltip, Legend } from "chart.js";
Chart.register(ArcElement, Tooltip, Legend);

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
    const { user } = useContext(AuthContext);
    const isAdmin = user?.role === "Admin";
    const navigate = useNavigate();
    const[seats, setSeats] = useState([]);
    const[selectedSeats, setSelectedSeats] = useState([]);
    const[totalPrice, setTotalPrice] = useState(0);
    const[stats, setStats] = useState(null);
    const [buttonActive, setButtonActive] = useState(false);

    useEffect(() => {
    if (!showId) {
        console.error("No showId found, redirecting...");
        navigate("/reservations"); // Falls keine ShowId vorhanden ist, zurück zur Show-Auswahl
        return;
    }

    fetchSeats(showId).then(setSeats);
}, [showId]);


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
        setTotalPrice(newTotalPrice);

        // Cambiar estado del botón dependiendo de la selección de asientos
        setButtonActive(selectedSeats.length > 0);
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

    const fetchShowStats = useCallback(async () => {
        if(!showId){
            return;
        }
        try{
            const response = await fetch(`http://127.0.0.1:5000/api/show_stats?show_id=${showId}`);
            const data = await response.json();
            if(data.success){
                setStats(data);
            }
        }
        catch(error){
            console.error("Error fetching show stats:", error);
        }
    }, [showId]);

    useEffect(() => {
        fetchShowStats();
    }, [fetchShowStats]);

    const handleReservation = async() => {
        if (!user) {
            alert("You need to log in first!");
            navigate("/login");
            return;
        }

        if (!user.id) {
        console.error("User-ID fehlt! User-Daten:", user);
        return;
        }

        if(selectedSeats.length === 0){
            alert("Please select a seat.");
            return;
        }

        const confirmBooking = window.confirm("Are you sure, you want to continue?");
        if(!confirmBooking){
            return;
        }

        console.log("Reservierung wird gestartet für:", user.id, selectedSeats);

        const result = await  reserveSeats(user.id, showId, selectedSeats);

        if(result.success){
            navigate("/booking-confirmation", {
                state: {
                    reservationId: result.reservationId,
                    totalPrice: totalPrice,
                },
            });
        }
        else{
            alert(`error reserving: ${result.message}`);
        }
    };

    const deleteReservation = async (seatId) => {
        try{
            const response = await fetch(`http://127.0.0.1:5000/api/delete_reservation?seat_id=${seatId}`, {
                method: "DELETE",
            });

            const data = await response.json();
            if(data.success){
                alert("Reservation deleted successfully");
                fetchSeats(showId).then(setSeats);
                fetchShowStats();
            }
        }
        catch(error){
            console.error("Error deleting reservation:", error);
        }
    };

        return (
        <div className="seat-page">
            {isAdmin && stats && (
                <div className="admin-stats">
                    <h3>Show Statistics</h3>
                    <p>Available Seats: {stats.available_seats}</p>
                    <p>Booked Seats: {stats.booked_seats}</p>
                    <p>Total Revenue: €{stats.revenue.toFixed(2)}</p>
                </div>
            )}
            <h2 className="seat-title">Seat Selection</h2>
            <div className="seat-container">
                <div className="row-numbers">
                    {Array.from(new Set(seats.map(seat => seat.row_number))).map(row => (
                        <div key={row} className="row-number">{row}</div>
                    ))}
                </div>
                <div className="seat-grid">
                    {seats.length > 0 ? (
                        seats.map((seat) => (
                            <div
                                key={seat.id}
                                className={`seat ${seat.isbooked ? "seat-booked" : "seat-free"} ${selectedSeats.includes(seat.id) ? "seat-selected" : ""}`}
                                onClick={() => {
                                    if (!seat.isbooked) {
                                        toggleSeatSelection(seat.id, Number(seat.price) || 0);
                                    } else if (isAdmin) {
                                        const confirmDelete = window.confirm("Do you want to delete this reservation?");
                                        if (confirmDelete) {
                                            deleteReservation(seat.id);
                                        }
                                    }
                                }}
                            >
                                <MdEventSeat />
                                <span className="seat-tooltip">Row {seat.row_number} - Seat {seat.seat_number}</span>
                            </div>
                        ))
                    ) : (
                        <p>Loading seats...</p>
                    )}
                </div>
            </div>
            {isAdmin && stats && (
                <div className="chart-container">
                    <h3>Seat Availability</h3>
                    <Pie
                        className="pie-chart"
                        data={{
                            labels: ["Available Seats", "Booked Seats"],
                            datasets: [
                                {
                                    label: "Seats",
                                    data: [stats.available_seats, stats.booked_seats],
                                    backgroundColor: ["#4CAF50", "#E57373"],
                                },
                            ],
                        }}
                        options={{ responsive: true, maintainAspectRatio: false }}
                    />
                </div>
            )}
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
            {!isAdmin && (
                <button
                    className={`booking-button ${selectedSeats.length > 0 ? "active" : ""}`}
                    disabled={selectedSeats.length === 0}
                    onClick={handleReservation}
                >
                    Book Now!
                </button>
            )}
        </div>
    );

}
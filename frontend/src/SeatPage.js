import React, { useEffect, useState, useContext } from "react";
import './SeatPage.css';
import { MdEventSeat } from "react-icons/md";
import { useParams, useNavigate } from "react-router-dom";
import reserveSeats from "./Reservation";
import { AuthContext } from "./AuthContext";
import { Pie } from "react-chartjs-2";
import { IoArrowBackOutline } from "react-icons/io5";

import { Chart, ArcElement, Tooltip, Legend } from "chart.js";
Chart.register(ArcElement, Tooltip, Legend);

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

const fetchShowStats = async (showId, setStats) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/show_stats?show_id=${showId}`);
        const data = await response.json();
        if (data.success) {
            setStats(data);
        }
    } catch (error) {
        console.error("Error fetching show stats:", error);
    }
};

export default function SeatSelection() {
    const { showId } = useParams();
    const { user } = useContext(AuthContext);
    const isAdmin = user?.role === "Admin";
    const navigate = useNavigate();
    const [seats, setSeats] = useState([]);
    const [selectedSeats, setSelectedSeats] = useState([]);
    const [totalPrice, setTotalPrice] = useState(0);
    const [stats, setStats] = useState(null);
    const [showChart, setShowChart] = useState(false);

    useEffect(() => {
        if (!showId) {
            navigate("/reservations");
            return;
        }
        fetchSeats(showId).then(setSeats);
        fetchShowStats(showId, setStats);
    }, [showId]);

    useEffect(() => {
        setTotalPrice(selectedSeats.reduce((acc, seatId) => {
            const seat = seats.find(s => s.id === seatId);
            return acc + (seat ? Number(seat.price) : 0);
        }, 0));
    }, [selectedSeats, seats]);

    const toggleSeatSelection = (seatId) => {
        setSelectedSeats((prevSelectedSeats) => {
            if (prevSelectedSeats.includes(seatId)) {
                return prevSelectedSeats.filter(id => id !== seatId);
            } else {
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

            <button className="back-button-2" onClick={() => navigate(-1)}>
                <IoArrowBackOutline />
            </button>

            <h2 className="seat-title">Seat Selection</h2>
            <div className="seat-container">
                <div className="row-numbers">
                    {seats.length > 0 && Array.from(new Set(seats.map(seat => seat.row_number))).map(row => (
                        <div key={row} className="row-number">{row}</div>
                    ))}
                </div>
                <div className="seat-grid">
                    {seats.length > 0 ? (
                        seats.map((seat) => (
                            <div
                                key={seat.id}
                                className={`seat ${seat.isbooked ? "seat-booked" : "seat-free"} ${selectedSeats.includes(seat.id) ? "seat-selected" : ""}`}
                                onClick={() => !seat.isbooked && toggleSeatSelection(seat.id)}
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
            <div className="screen"></div>
            <div className="summary">
                {selectedSeats.length > 0 && (
                    <>
                        <p>Selected Seats: {selectedSeats.join(", ")}</p>
                        <p><strong>Total Price: €{totalPrice.toFixed(2)}</strong></p>
                    </>
                )}
            </div>
            <button
                className={`booking-button ${selectedSeats.length > 0 ? "active" : ""}`}
                disabled={selectedSeats.length === 0}
                onClick={handleReservation}
            >
                Book Now!
            </button>
            {isAdmin && (
                <button
                    className="admin-button"
                    onClick={() => setShowChart(!showChart)}
                >
                    {showChart ? "Hide Chart" : "Show Chart"}
                </button>
            )}
            {isAdmin && showChart && stats && (
                <div className="chart-container">
                    {/* Sección de texto dentro del mismo recuadro */}
                    <div className="chart-text">
                        <h3>Seat Availability</h3>
                        <p>Available Seats: {stats.available_seats}</p>
                        <p>Booked Seats: {stats.booked_seats}</p>
                        <p>Total Revenue: €{stats.revenue.toFixed(2)}</p>
                    </div>

                    {/* Gráfico dentro del mismo recuadro */}
                    <div className="chart-graph">
                       <Pie
    data={{
        labels: ["Available Seats", "Booked Seats"],
        datasets: [{
            data: [stats.available_seats, stats.booked_seats],
            backgroundColor: ["#4CAF50", "#E57373"],
        }],
    }}
    options={{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: "white", // Cambia el color del texto de la leyenda
                    font: {
                        size: 14 // Tamaño de la fuente opcional
                    }
                }
            },
            tooltip: {
                bodyFont: {
                    size: 14
                },
                titleFont: {
                    size: 16
                },
                titleColor: "white", // Cambia el color del título del tooltip
                bodyColor: "white" // Cambia el color del cuerpo del tooltip
            }
        }
    }}
/>

                    </div>
                </div>
            )}
        </div>
    );
}
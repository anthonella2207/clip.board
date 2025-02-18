import React, { useEffect, useState } from "react";
import { PiListMagnifyingGlass } from "react-icons/pi";
import "./BookingPage.css";
import { IoArrowBackOutline } from "react-icons/io5";
import { Link } from "react-router-dom";
import { QRCodeCanvas } from "qrcode.react";

const BookingPage = ({ userId }) => {
  // State variables for bookings, loading state, and errors
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completedBookings, setCompletedBookings] = useState(new Set());

  // Load completed bookings from localStorage when component mounts
  useEffect(() => {
    const storedCompleted = JSON.parse(localStorage.getItem("completedBookings")) || {};
    setCompletedBookings(new Set(storedCompleted[userId] || []));
  }, [userId]);

  // Fetch user bookings from the API
  useEffect(() => {
    if (!userId) return;

    fetch(`http://127.0.0.1:5000/api/bookings/${userId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          setBookings(data.bookings);
        }
        setLoading(false);
      })
      .catch((error) => {
        console.error("Fetch Error:", error);
        setError("An error occurred while loading bookings.");
        setLoading(false);
      });
  }, [userId]);

  // Save completed bookings to localStorage whenever the state changes
  useEffect(() => {
    const storedCompleted = JSON.parse(localStorage.getItem("completedBookings")) || {};
    storedCompleted[userId] = Array.from(completedBookings);
    localStorage.setItem("completedBookings", JSON.stringify(storedCompleted));
  }, [completedBookings, userId]);

  // Show loading message if bookings are still being fetched
  if (loading) {
    return <p>Loading bookings...</p>;
  }
  if (error) {
    return <p>Error: {error}</p>;
  }

  // Function to mark a booking as completed
const markAsCompleted = (bookingId) => {
  fetch("http://127.0.0.1:5000/api/bookings/cancel", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ booking_id: bookingId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        setBookings((prev) => prev.filter((booking) => booking.id !== bookingId));
      } else {
        console.error("Error cancelling:", data.message);
      }
    })
    .catch((error) => console.error("Network error:", error));
};

  // Function to cancel a booking with user confirmation
  const cancelBooking = (bookingId) => {
    if (!window.confirm("Are you sure you want to cancel this booking?")) {
      return;
    }

    fetch("http://127.0.0.1:5000/api/bookings/cancel", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ booking_id: bookingId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setBookings((prev) => prev.filter((booking) => booking.id !== bookingId));
        } else {
          console.error("Error cancelling:", data.message);
        }
      })
      .catch((error) => console.error("Network error:", error));
  };

  const currentBookings = bookings.filter((booking) => !completedBookings.has(booking.id));
  const pastBookings = bookings.filter((booking) => completedBookings.has(booking.id));

return (
  <>
    <div className="booking-page-title">My Bookings</div>
    <div className="booking-page">
      <Link to="/" className="back-link">
        <IoArrowBackOutline />
      </Link>

      {currentBookings.length === 0 ? (
        <p className="no-bookings">
          <PiListMagnifyingGlass />
        </p>
      ) : (
        <>
          {/* Current Bookings Section */}
          {currentBookings.length > 0 && <h3 className="section-title">Current Bookings</h3>}
            <div className="booking-list">
              {currentBookings.map((booking) => (
                <div key={booking.id} className="booking-ticket active">
                  <div className="ticket-text">
                    <strong>{booking.movie_name}</strong>
                    <p>{booking.show_time} - Hall: {booking.hall}</p>
                    <p>Reservation #{booking.id}</p>
                  </div>
                  <div className="ticket-footer">
                    <QRCodeCanvas value={booking.id.toString()} className="qr-code" />
                    <div className="ticket-buttons">
                      <button onClick={() => markAsCompleted(booking.id)}>Done</button>
                      <button onClick={() => cancelBooking(booking.id)}>Cancel</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
        </>
      )}
    </div>
  </>
);
};

export default BookingPage;

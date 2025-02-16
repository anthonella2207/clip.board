import React, { useEffect, useState } from "react";
import { PiListMagnifyingGlass } from "react-icons/pi";
import "./BookingPage.css";
import {IoArrowBackOutline} from "react-icons/io5";
import {Link} from "react-router-dom";

const BookingPage = ({ userId }) => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completedBookings, setCompletedBookings] = useState(new Set());

  useEffect(() => {
    const storedCompleted = JSON.parse(localStorage.getItem("completedBookings")) || {};
    setCompletedBookings(new Set(storedCompleted[userId] || []));
  }, [userId]);

  useEffect(() => {
    if (!userId) {
      return;
    }

    fetch(`http://127.0.0.1:5000/api/bookings/${userId}`)
      .then((response) => {
        console.log("API Response:", response);

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }

        return response.json();
      })
      .then((data) => {
        console.log("Parsed JSON:", data);
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

  useEffect(() => {
    const storedCompleted = JSON.parse(localStorage.getItem("completedBookings")) || {};
    storedCompleted[userId] = Array.from(completedBookings);
    localStorage.setItem("completedBookings", JSON.stringify(storedCompleted));
  }, [completedBookings, userId]);

  if (loading) {
    return <p>Loading bookings...</p>;
  }
  if (error) {
    return <p>Error: {error}</p>;
  }

  const currentBookings = bookings.filter((booking) => !completedBookings.has(booking.id));

  const pastBookings = bookings.filter((booking) => completedBookings.has(booking.id));

  const markAsCompleted = (bookingId) => {
    setCompletedBookings((prev) => new Set([...prev, bookingId]));
  };

  const cancelBooking = (bookingId, showId) => {
    if (!window.confirm("Are you sure you want to cancel this booking?")) {
      return;
    }

    fetch("http://127.0.0.1:5000/api/bookings/cancel", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ booking_id: bookingId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Reservation cancelled");

          // Remove the booking from the list
          setBookings((prevBookings) => prevBookings.filter((booking) => booking.id !== bookingId));

          // Reload seats
          fetchSeats(showId).then(setSeats);

          // Reload statistics
          fetchStatistics("occupancy");
        } else {
          console.error("Error cancelling:", data.message);
        }
      })
      .catch((error) => console.error("Network error:", error));
  };

  return (
    <div className={"booking-page"}>
      <Link to="/" className="back-link">
        <IoArrowBackOutline />
      </Link>
      <h2>My bookings</h2>

      {bookings.length === 0 ? (
          <p className="no-bookings"><PiListMagnifyingGlass /></p>
      ) : (
        <>
          <h3>Current bookings</h3>
          {currentBookings.length === 0 ? (
            <p>No current bookings</p>
          ) : (
            <ul>
              {currentBookings.map((booking) => (
                <li key={booking.id}>
                  <strong>{booking.movie_name}</strong> - {booking.show_time} - Hall: {booking.hall} - Reservation
                  number: {booking.id}
                  <button onClick={() => markAsCompleted(booking.id)}>Done</button>
                  <button onClick={() => cancelBooking(booking.id, booking.show_id)}>Cancel booking</button>
                </li>
              ))}
            </ul>
          )}

          <h3>Past bookings</h3>
          {pastBookings.length === 0 ? (
            <p>No past bookings so far</p>
          ) : (
            <ul>
              {pastBookings.map((booking) => (
                <li key={booking.id}>
                  <strong>{booking.movie_name}</strong> - {booking.show_time} - Hall: {booking.hall} - Reservation number: {booking.id}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
};

export default BookingPage;
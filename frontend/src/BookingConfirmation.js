import React, { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import { QRCodeCanvas } from "qrcode.react";
import "./BookingConfirmation.css";
import { CiCircleCheck } from "react-icons/ci";

const BookingConfirmation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { reservationId, totalPrice } = location.state || {};
    const { logout } = useContext(AuthContext);
    const currentDate = new Date().toLocaleDateString("en-US", {
        day: "2-digit", month: "short", year: "2-digit"
    });

    const handleGoToBookings = () => {
        navigate("/bookings");
    };

    if (!reservationId) {
        return <p className="error-message">No booking found</p>;
    }

    return (
        <div className="booking-ticket-container">
            <div className="ticket">
                <div className="ticket-header">
                    <h2>Booking Confirmed!</h2>
                </div>
                <div className="ticket-body">
                    <p className="warning-text">Please bring your reservation number to your visit.</p>
                    <div className="booking-details">
                        <div>
                            <p className="label">Reservation #</p>
                            <p className="value">{reservationId}</p>
                        </div>
                        <div>
                            <p className="label">Total Price</p>
                            <p className="value">${totalPrice}</p>
                        </div>
                        <div>
                            <p className="label">Date</p>
                            <p className="value">{currentDate}</p>
                        </div>
                    </div>
                </div>
                <div className="ticket-footer">
                    <QRCodeCanvas value={reservationId.toString()} className="qr-code" />
                </div>
            </div>
           <button className="goToBookings-button" onClick={handleGoToBookings}><CiCircleCheck /></button>
        </div>
    );
};

export default BookingConfirmation;

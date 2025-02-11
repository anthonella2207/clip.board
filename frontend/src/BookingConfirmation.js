import React, { useContext } from "react";
import {useNavigate, useLocation} from "react-router-dom";
import {AuthContext} from "./AuthContext";
import "./BookingConfirmation.css";

const BookingConfirmation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const {reservationId, totalPrice} = location.state || {};
    const { logout } = useContext(AuthContext);

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    if(!reservationId){
        return <p>No booking found</p>;
    }

    return (
        <div className="booking-confirmation-container">
            <div className="confirmation-box">
                <h2 className="confirmation-title">Booking Confirmed!</h2>
                <p className="confirmation-text warning-text">
                    Please bring your reservation number to your visit.
                </p>
                <p className="confirmation-text">Your reservation number:</p>
                <div className="booking-number">#{reservationId}</div>
                <p className="confirmation-text">Total Price: ${totalPrice}</p>
                <button className="logout-button" onClick={handleLogout}>Logout</button>
            </div>
        </div>
    );
};

export default BookingConfirmation;
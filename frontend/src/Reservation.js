import React from "react";

const reserveSeats = async(userId, showId, seatIds) => {
    try{
        const response = await fetch("http://127.0.0.1:5000/api/reserve", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                user_id: userId,
                show_id: showId,
                seat_ids: seatIds,
            }),
        });

        const data = await response.json();
        if(data.success){
            return{success: true, reservationId: data.reservation_id, totalPrice: data.total_price};
        }
        else{
            return{success: false, message: data.message};
        }
    }
    catch (error){
        return{success: false, message: "server error"};
    }
};

export default reserveSeats;
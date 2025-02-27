import PropTypes from "prop-types";
import "../styles/Booking.css"; // Import the CSS file
import { useState, useEffect } from "react";

const Booking = ({booking}) => {
    const {
        id,
        date,
        hour,
        ticket,
        type_of_service,
        created_at,
        client_username,
    } = booking;
    const [is_expired, setIsExpired] = useState(false);

    useEffect(() => {
        if (!date) return;

        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const bookingDate = new Date(date + "T00:00:00"); // Forces local time
        bookingDate.setHours(0, 0, 0, 0);

        if (bookingDate < today) {
            setIsExpired(true);
        } else {
            setIsExpired(false);
        }
    }, [date]);


    return (
        <div className={`booking ${is_expired ? "used" : "pending"}`}>
            <span><strong>Username:</strong> {client_username}</span>
            {type_of_service === "classes" && <span><strong>Hour:</strong> {hour}</span>}
            <span><strong>Date:</strong> {date}</span>
            <span><strong>Ticket:</strong> {ticket}</span>
            <span><strong>Activity:</strong> {type_of_service}</span>
            <span><strong>Created At:</strong> {new Date(created_at).toLocaleString()}</span>
        </div>
    );
};

Booking.propTypes = {
    booking: PropTypes.shape({
        id: PropTypes.number.isRequired,
        client: PropTypes.number.isRequired,
        date: PropTypes.string.isRequired,
        hour: PropTypes.string,
        ticket: PropTypes.number.isRequired,
        type_of_service: PropTypes.string.isRequired,
        created_at: PropTypes.string.isRequired,
        client_username: PropTypes.string.isRequired,
    }).isRequired,
};

export default Booking;
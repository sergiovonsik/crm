import PropTypes from "prop-types";
import "../styles/Booking.css"; // Import the CSS file
import { useState, useEffect } from "react";

const Price = ({data}) => {
    const {
        id,
        price,
        type_of_service,
        pass_amount,
    } = data;
    return (
        <div className={`booking pending`}>
            <span><strong>ID:</strong> {id}</span>
            <span><strong>Price:</strong> ${price}</span>
            <span><strong>amount of passes:</strong> {pass_amount}</span>
            <span><strong>Activity:</strong> {type_of_service}</span>
        </div>
    );
};

Price.propTypes = {
    data: PropTypes.shape({
        id: PropTypes.number.isRequired,
        price: PropTypes.number.isRequired,
        pass_amount: PropTypes.number.isRequired,
        type_of_service: PropTypes.string.isRequired,
    }).isRequired,
};

export default Price;
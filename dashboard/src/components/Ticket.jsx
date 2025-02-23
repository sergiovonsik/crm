import React from "react";
import "../styles/Ticket.css"; // Import the CSS file

import PropTypes from "prop-types";

const Ticket = ({ ticket }) => {
  const {
    id,
    type_of_service,
    amount_of_uses_LEFT,
    payment_day,
    expire_time,
    is_expired,
  } = ticket;

  return (
    <div className={`ticket ${is_expired ? "expired" : "valid"}`}>
      <span><strong>ID:</strong> {id}</span>
      <span><strong>Service:</strong> {type_of_service}</span>
      <span><strong>Uses Left:</strong> {amount_of_uses_LEFT}</span>
      <span><strong>Valid from:</strong> {payment_day} to {expire_time}</span>
      <span className="status">
        {is_expired ? "❌ Expired" : "✅ Valid"}
      </span>
    </div>
  );
};

Ticket.propTypes = {
  ticket: PropTypes.shape({
    id: PropTypes.number.isRequired,
    type_of_service: PropTypes.string.isRequired,
    amount_of_uses_LEFT: PropTypes.number.isRequired,
    payment_day: PropTypes.string.isRequired,
    expire_time: PropTypes.string.isRequired,
    is_expired: PropTypes.bool.isRequired,
  }).isRequired,
};

export default Ticket;

/*
'amount_of_uses_LEFT': 7,
                     'expire_time': '2025-03-04',
                     'is_expired': False,
                     'owner': 2,
                     'type_of_service': 'classes'}
*/
import React from "react";
import "../styles/Ticket.css"; // Import the CSS file

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

export default Ticket;

/*
'amount_of_uses_LEFT': 7,
                     'expire_time': '2025-03-04',
                     'is_expired': False,
                     'owner': 2,
                     'type_of_service': 'classes'}
*/
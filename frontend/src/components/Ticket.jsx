import React from "react";
import "../styles/Ticket.css"; // Import the CSS file

const Ticket = ({ ticket }) => {
  const {
    id,
    type_of_service,
    amount_of_uses_LEFT,
    expire_time,
    is_expired,
    payment_day,
  } = ticket;

  return (
    <div className={`ticket ${is_expired ? "expired" : "valid"}`}>
      <span><strong>ID:</strong> {id}</span>
      <span><strong>Service:</strong> {type_of_service}</span>
      <span><strong>Uses Left:</strong> {amount_of_uses_LEFT}</span>
      <span><strong>Expires:</strong> {expire_time}</span>
      <span><strong>Payment:</strong> {payment_day}</span>
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
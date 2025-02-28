import Ticket from "./Ticket.jsx";
import Booking from "./Booking.jsx";

import PropTypes from "prop-types";

function SelectedUserData({selectedUserData, paymentTickets, bookingFiles, setTicketsFilter,
                        ticketsFilter, setBookingFilter, bookingFilter}) {

    function showTicketsInUse(tickets = paymentTickets) {
        return tickets
            .filter(ticket => !ticket.is_expired)
    }

    function showPendingBookings(bookings = bookingFiles) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        return bookings.filter(booking => {
            const bookingDate = new Date(booking.date + "T00:00:00"); // Forces local time
            bookingDate.setHours(0, 0, 0, 0);

            return bookingDate >= today; // Faltaba el `return`
        });
    }

    return (
    <div>
        <div className="profile-container">
            <h2>User Profile</h2>
            <div className="profile-box">
                <p><strong>Username:</strong>
                    {selectedUserData.username}
                </p>
                <p><strong>ID:</strong>
                    {selectedUserData.pk}
                </p>
                <p><strong>Date Joined:</strong>
                    {new Date(selectedUserData.date_joined).toLocaleDateString("en-GB")}
                </p>
            </div>
        </div>
        <div>
            <div>
                <h2 className="titles">Tickets:</h2>

                <button className="filterButton" onClick={() => setTicketsFilter(!ticketsFilter)}>
                    {ticketsFilter ? "Show All" : "Hide Expired"} Tickets
                </button>
            </div>
            {Array.isArray(paymentTickets) && paymentTickets.length > 0 ? (
                ticketsFilter ? (
                    showTicketsInUse().map((ticket) => (
                        <Ticket ticket={ticket} key={ticket.id}/>
                    ))
                ) : (
                    paymentTickets.map((ticket) => (
                        <Ticket ticket={ticket} key={ticket.id}/>
                    ))
                )
            ) : (
                <p>No tickets found.</p>
            )}
        </div>
        <div>
            <div >
                <h2 className="titles">Bookings:</h2>

                <button className="filterButton" onClick={() => setBookingFilter(!bookingFilter)}>
                    {bookingFilter ? "Show All" : "Hide Expired"} Bookings
                </button>
            </div>
            {Array.isArray(bookingFiles) && bookingFiles.length > 0 ? (
                bookingFilter ? (
                    showPendingBookings().map((booking) => (
                        <Booking booking={booking} key={booking.id}/>
                    ))
                ) : (
                    bookingFiles.map((booking) => (
                        <Booking booking={booking} key={booking.id}/>
                    ))
                )
            ) : (
                <p>No bookings found.</p>
            )}
        </div>

    </div>)
}


SelectedUserData.propTypes = {
    selectedUserData: PropTypes.shape({
        username: PropTypes.string,
        date_joined: PropTypes.string,
        pk: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
    paymentTickets: PropTypes.arrayOf(PropTypes.object),
    bookingFiles: PropTypes.arrayOf(PropTypes.object),
    setTicketsFilter: PropTypes.func.isRequired,
    ticketsFilter: PropTypes.bool.isRequired,
    setBookingFilter: PropTypes.func.isRequired,
    bookingFilter: PropTypes.bool.isRequired
};

export default SelectedUserData;
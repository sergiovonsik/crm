import { useState, useEffect } from "react";
import api from "../api";
import Ticket from "../components/Ticket";
import Sidebar from "../components/Sidebar";
import "../styles/Home.css";
import Booking from "../components/Booking.jsx";

function Home() {
    const [paymentTickets, setPaymentTickets] = useState([]);
    const [ticketsFilter, setTicketsFilter] = useState(true);
    const [bookingFiles, setBookingFiles] = useState([]);
    const [bookingFilter, setBookingFilter] = useState(true);
    const [user , setUser ] = useState({});

    useEffect(() => {
        getUserData();
    }, []);

    function showTicketsInUse(tickets = paymentTickets) {
        return tickets
            .filter(ticket => !ticket.is_expired)
    }

    function showPendingBookings(bookings = bookingFiles) {
        const today = new Date()
        ;return bookings
            .filter(booking => new Date(booking.date) >= today)

    }
    
    
    const getUserData = async () => {
        try {
            const res = await api.get(`/api/user/me/info/`);
            const data = res.data;
            const userObjectData = {
                'username': data.username,
                'id': data.id,
                'date_joined': data.date_joined,
                'last_login': data.last_login,
            };

            let booking_tickets = data.bookings;
            booking_tickets.sort((a, b) => new Date(a.date) - new Date(b.date));
            sessionStorage.setItem("bookingFiles", JSON.stringify(booking_tickets)); // Save to sessionStorage
            setBookingFiles(booking_tickets || []);

            let payment_ticket = data.payment_ticket;
            payment_ticket.sort((a, b) => new Date(a.expire_time) - new Date(b.expire_time));
            sessionStorage.setItem("payment_ticket", JSON.stringify(payment_ticket)); // Save to sessionStorage
            setPaymentTickets(payment_ticket || []);

            setUser(userObjectData)

            console.log(data);
        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
                <div className="profile-container">
                    <h2>User Profile</h2>
                    <div className="profile-box">
                        <p><strong>Username:</strong>
                            {user.username}
                        </p>
                        <p><strong>ID:</strong>
                            {user.id}
                        </p>
                        <p><strong>Date Joined:</strong>
                            {new Date(user.date_joined).toLocaleDateString("en-GB")}
                        </p>
                    </div>
                </div>

                <div>
                    <div className="inline-elements">
                        <h2 className="titles">Tickets:</h2>
                        
                        <button className="filterButton" onClick={() => setTicketsFilter(!ticketsFilter)}>
                             {ticketsFilter ? "Hide Expired" : "Show All"} Tickets
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
                    <div className="inline-elements">
                        <h2 className="titles">Bookings:</h2>

                        <button className="filterButton" onClick={() => setBookingFilter(!bookingFilter)}>
                            {bookingFilter ? "Hide Expired" : "Show All"} Bookings
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
            </div>
        </div>
    );
}

export default Home;
 
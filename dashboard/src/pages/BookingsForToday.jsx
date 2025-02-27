import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/SearchUser.css";
import Booking from "../components/Booking.jsx";
import api from "../api.js";

function BookingsForToday() {
    const [bookings, setBookings] = useState([]);
    const [numberOfClosedItems, setNumberOfClosedItems] = useState(0);

    useEffect(() => {
            getBookingData();
    }, []);

    const getBookingData = async () => {
        try {
            const res = await api.get(`api/userAdmin/todayPasses/`);
            const bookingData = res.data.booking_files;

            console.log(res.data);

            setNumberOfClosedItems(0);
            setBookings(bookingData);
        } catch (err) {
            console.error("Error fetching Bookings:", err);
            alert("Failed to load tickets.");
            setNumberOfClosedItems(0);
            setBookings([]);
        }
    };

    const deleteBox = (id) => {
        const userConfirmed = window.confirm("Are you sure you want to close the notification?");
        if (userConfirmed) {
            console.log("User confirmed!");
            const newBookingFiles = bookings.filter(booking => booking.id !== id);
            setBookings(newBookingFiles);
            setNumberOfClosedItems(numberOfClosedItems + 1)

            setBookings(newBookingFiles);
        }
    }

    const resetClosedBoxes = () => {
        getBookingData();
    }

    return (
        <div>
            <Sidebar />
            <div className="main-content">
                <div className="inline-elements">
                    <div className="inner-container">
                        <div  className="reset-button" onClick={() => resetClosedBoxes()}>
                            Reset
                        </div>
                    </div><div className="inner-container">
                        <div className="title">Pending bookings for today:</div>
                        <div className="number-box">{bookings.length}</div>
                    </div>
                    <div className="inner-container">
                        <div className="title">Already checked:</div>
                        <div className="number-box">{numberOfClosedItems}</div>
                    </div>

                </div>
                <div className="dashboard">
                    {bookings.length > 0 ? (
                        bookings.map((booking) => (
                            <div onClick={() => deleteBox(booking.id)} key={booking.id}>
                                <Booking booking={booking} />
                            </div>
                        ))
                    ) : (
                        <p>No bookings found.</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default BookingsForToday;

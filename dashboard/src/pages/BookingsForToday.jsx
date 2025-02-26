import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/AssignPasses.css";
import Booking from "../components/Booking.jsx";
import api from "../api.js";

function BookingsForToday() {
    const [bookings, setBookings] = useState([]);

    useEffect(() => {
        const storedBookings = sessionStorage.getItem("bookingFiles");

        if (!storedBookings) {
            getBookingData();
        } else {
            setBookings(JSON.parse(storedBookings));
        }

        if (!sessionStorage.getItem("numberOfClosedItems")) {
            sessionStorage.setItem("numberOfClosedItems", JSON.stringify(0));
        }
    }, []);

    const getBookingData = async () => {
        try {
            const res = await api.get(`api/userAdmin/todayPasses/`);
            const bookingData = res.data.booking_files;

            sessionStorage.setItem("bookingFiles", JSON.stringify(bookingData));
            sessionStorage.setItem("numberOfClosedItems", JSON.stringify(0));
            setBookings(bookingData);
        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };

    const deleteBox = (id) => {
        const userConfirmed = window.confirm("Are you sure you want to close the notification?");
        if (userConfirmed) {
            console.log("User confirmed!");

            const storedBookings = JSON.parse(sessionStorage.getItem("bookingFiles")) || [];
            const numberOfClosedItems = JSON.parse(sessionStorage.getItem("numberOfClosedItems"));
            const newBookingFiles = storedBookings.filter(booking => booking.id !== id);

            sessionStorage.setItem("bookingFiles", JSON.stringify(newBookingFiles));
            sessionStorage.setItem("numberOfClosedItems", JSON.stringify(numberOfClosedItems + 1));

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
                        <div className="number-box">{sessionStorage.getItem("numberOfClosedItems")}</div>
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

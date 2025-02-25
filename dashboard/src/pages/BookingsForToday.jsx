import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/AssignPasses.css";
import Booking from "../components/Booking.jsx";
import api from "../api.js";

function  BookingsForToday() {
    const [bookingFiles, setBookingFiles] = useState([]);


    useEffect(() => {
        getBookingData();
    }, [])

    const getBookingData = async () => {
        try {
            const res = await api.get(`api/userAdmin/todayPasses/`);
            const bookingData = res.data.booking_files;
            setBookingFiles(bookingData || []);
            console.log(bookingData);


        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };

    function deleteBox(id){
        alert("Booking deleted");
        setBookingFiles(bookingFiles.filter(booking => booking.id !== id));
    }

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
                <div className="inline-elements">
                    <div className="title">Bookings for today:</div>
                    <div className="number-box">
                        {bookingFiles.length}
                    </div>

                </div>
                <div className="dashboard">
                    {bookingFiles.length > 0 ? (
                        bookingFiles.map((booking) => (
                            <div onClick={() => {deleteBox(booking.id)}} key={booking.id}>
                                <Booking
                                    booking={booking}

                                />
                            </div>
                        ))
                    ) : (<p>No bookings found.</p>)
                    }
                </div>
            </div>
        </div>
    );
}

export default BookingsForToday;


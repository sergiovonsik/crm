import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/BuyPasses.css";
import BookingForm from "../components/BookingForm.jsx";
import { parseISO } from "date-fns";

function BookPass() {
    const [bookedDays, setBookedDays] = useState( [parseISO("2025-02-22"), parseISO("2025-02-25")]);

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
                <div className="dashboard">
                    < BookingForm />
                </div>
            </div>
        </div>
    );
}

export default BookPass;


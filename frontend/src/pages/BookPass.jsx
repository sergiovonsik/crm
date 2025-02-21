import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/BuyPasses.css";
import BookingForm from "../components/BookingForm.jsx";
import { parseISO } from "date-fns";

function BookPass() {
    const [bookedDays, setBookedDays] = useState( [parseISO("2025-02-22"), parseISO("2025-02-25")]);
    const [errorInfo, setErrorInfo] = useState("");

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
              {
                errorInfo !== "" &&
                (<div className="error-message">
                  {errorInfo}
                </div>)
              }
                <div className="dashboard">
                    < BookingForm setErrorInfo={setErrorInfo}/>
                </div>
            </div>
        </div>
    );
}

export default BookPass;


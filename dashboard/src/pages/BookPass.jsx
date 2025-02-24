import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/AssignPasses.css";
import BookingForm from "../components/BookingForm.jsx";

function BookPass() {
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


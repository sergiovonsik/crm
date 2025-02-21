import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../styles/Form.css";
import LoadingIndicator from "./LoadingIndicator";
import api from "../api";

function BookingForm() {
    const [type_of_service, setType_of_service] = useState("");
    const [date, setDate] = useState(null);
    const [hour, setHour] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const res = await api.post("api/user/book_pass/", {
                type_of_service,
                date: date?.toISOString().split("T")[0],  // Format date as YYYY-MM-DD
                hour
            });
            console.log(res.data);
            if (res.status === 201) {
                alert("Successfully booked.");
                navigate("/");

            } else {
                alert("Failed to load tickets.");
                navigate("/book_pass");}
        } catch (error) {
            alert("Booking failed: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Book an Activity</h1>

            {/* Activity Type Dropdown */}
            <select
                className="form-input"
                value={type_of_service}
                onChange={(e) => setType_of_service(e.target.value)}
                required
            >
                <option value="">Select Activity Type</option>
                <option value="classes">Class</option>
                <option value="free_climbing">Free Climbing</option>
            </select>

            {/* Date Picker */}
            <DatePicker
                selected={date}
                onChange={(selectedDate) => setDate(selectedDate)}
                dateFormat="yyyy-MM-dd"
                className="form-input"
                placeholderText="Select Date"
                filterDate={(date) => date.getDay() !== 0}  // Disable Saturdays (6) and Sundays (0)
                required
            />

            {/* Hour input (only for classes) */}
            {type_of_service === "classes" && (
                <select
                    className="form-input"
                    type="time"
                    value={hour}
                    onChange={(e) => setHour(e.target.value)}
                    required>
                    <option value="">Select hour range</option>
                    <option value="6 to 8">6 to 8</option>
                    <option value="8 to 10">8 to 10</option>
                </select>
            )}

            {loading && <LoadingIndicator />}

            <button className="form-button" type="submit" disabled={!type_of_service || !date}>
                Submit
            </button>
        </form>
    );
}

export default BookingForm;

import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Home.css";
import Sidebar from "../components/Sidebar";
import LineChartComponent from "../components/LineChartComponent.jsx";
import DonutChartComponent from "../components/DonutChartComponent.jsx";
import RangeSlider from "../components/TimeSlider.jsx";
//import Ticket from "../components/Ticket";
//import Booking from "../components/Booking.jsx";

function BusinessData() {
    //const [bookingFilter, setBookingFilter] = useState(true);
    const [bookingChart, setBookingChart] = useState([]);
    const [ticketChart, setTicketChart] = useState([]);
    const [activeClientsChart, setActiveClientsChart] = useState([]);
    const [typeOfServiceChart, setTypeOfServiceChart] = useState([]);
    const [rangeOfDates, setRangeOfDates] = useState([-30, 0]);

    useEffect(() => {
        const end_day = new Date(new Date().setDate(new Date().getDate() + rangeOfDates[1]));
        const start_day = new Date(new Date().setDate(new Date().getDate() + rangeOfDates[0]));
        getBookingChartData(end_day, start_day);
        getTicketChartData(end_day, start_day);
        getActiveClientsChartData(end_day, start_day);
        getTypeOfServiceChartData(end_day, start_day);

    }, [rangeOfDates]);

    const getBookingChartData = async (end_day, start_day) => {
        try {
            const res = await api.post(`/api/userAdmin/BookingChart/`,
                {
                    end_day: end_day.toISOString().split('T')[0],
                    start_day: start_day.toISOString().split('T')[0],
                });
            const data = res.data.chart_data;
            setBookingChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };


    const getTicketChartData = async (end_day, start_day) => {
        try {
            const res = await api.post(`/api/userAdmin/TicketChart/`,
                {
                    end_day: end_day.toISOString().split('T')[0],
                    start_day: start_day.toISOString().split('T')[0],
                });
            const data = res.data.amount_per_day;
            setTicketChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };


    const getActiveClientsChartData = async (end_day, start_day) => {
        try {
            const res = await api.post(`/api/userAdmin/ActiveClientsChart/`,
                {
                    end_day: end_day.toISOString().split('T')[0],
                    start_day: start_day.toISOString().split('T')[0],
                });
            const data = res.data.chart_data;
            setActiveClientsChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };


    const getTypeOfServiceChartData = async (end_day, start_day) => {
        try {
            const res = await api.post(`/api/userAdmin/TypeOfServiceChartData/`,
                {
                    end_day: end_day.toISOString().split('T')[0],
                    start_day: start_day.toISOString().split('T')[0],
                });
            const data = res.data.chart_data;
            setTypeOfServiceChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
                <RangeSlider rangeOfDates={rangeOfDates} setRangeOfDates={setRangeOfDates}/>
                <h2>Clients Insights</h2>
                <div className="donut-container">
                    <div className="donut-box">
                        <DonutChartComponent title={'Services Used'}
                                             data={typeOfServiceChart}
                                             colors={["#7b00ff", "#1248a7", "#ffdf04", "#c80a18"]}/>
                    </div>
                    <div className="donut-box">
                        <DonutChartComponent title={'Active Clients'}
                                             data={activeClientsChart}
                                             colors={["#ffde04", "#c80a0a", "#ffdf04", "#c80a18"]}/>
                    </div>
                </div>
                <LineChartComponent title={'Bookings'} chartData={bookingChart} lineColor={"#f1c40f"}/>

                <LineChartComponent title={'Tickets Bought'} chartData={ticketChart} lineColor={"#7b00ff"}/>
            </div>
        </div>
    );
}

export default BusinessData;


/*
function showTicketsInUse(tickets = paymentTickets) {
        return tickets
            .filter(ticket => !ticket.is_expired)
    }

function showPendingBookings(bookings = bookingFiles) {
    const today = new Date()
    ;return bookings
        .filter(booking => new Date(booking.date) >= today)

}
 */
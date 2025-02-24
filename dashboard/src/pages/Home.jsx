import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Home.css";
import Sidebar from "../components/Sidebar";
import LineChartComponent from "../components/LineChartComponent.jsx";
import DonutChartComponent from "../components/DonutChartComponent.jsx";
import RangeSlider from "../components/TimeSlider.jsx";
//import Ticket from "../components/Ticket";
//import Booking from "../components/Booking.jsx";

function Home() {
    const [paymentTickets, setPaymentTickets] = useState([]);
    //const [ticketsFilter, setTicketsFilter] = useState(true);
    const [bookingFiles, setBookingFiles] = useState([]);
    //const [bookingFilter, setBookingFilter] = useState(true);
    const [bookingChart, setBookingChart] = useState([]);
    const [ticketChart, setTicketChart] = useState([]);
    const [activeClientsChart, setActiveClientsChart] = useState([]);
    const [typeOfServiceChart, setTypeOfServiceChart] = useState([]);
    const [rangeOfDates, setRangeOfDates] = useState([-30, 0]);
    const [user , setUser ] = useState({});

    useEffect(() => {
        const init_day = new Date(new Date().setDate(new Date().getDate() - rangeOfDates[1]));
        getUserData();
        getBookingChartData(init_day, -rangeOfDates[0]);
        getTicketChartData(init_day, -rangeOfDates[0]);
        getActiveClientsChartData(init_day, -rangeOfDates[0]);
        getTypeOfServiceChartData(init_day, -rangeOfDates[0]);

    }, [rangeOfDates]);


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

        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };


    const getBookingChartData = async (init_day, days_lapse) => {
        try {
            const res = await api.post(`/api/userAdmin/BookingChart/`,
                {
                    init_day: init_day.toISOString().split('T')[0],
                    days_lapse: days_lapse,
                });
            const data = res.data.amount_per_day;
            setBookingChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };


    const getTicketChartData = async (init_day, days_lapse) => {
        try {
            const res = await api.post(`/api/userAdmin/TicketChart/`,
                {
                    init_day: init_day.toISOString().split('T')[0],
                    days_lapse: days_lapse,
                });
            const data = res.data.amount_per_day;
            setTicketChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };


    const getActiveClientsChartData = async (init_day, days_lapse) => {
        try {
            const res = await api.post(`/api/userAdmin/ActiveClientsChart/`,
                {
                    init_day: init_day.toISOString().split('T')[0],
                    days_lapse: days_lapse,
                });
            const data = res.data.chart_data;
            setActiveClientsChart(data);
        } catch (err) {
            console.error("Error", err);
        }
    };


    const getTypeOfServiceChartData = async (init_day, days_lapse) => {
        try {
            const res = await api.post(`/api/userAdmin/TypeOfServiceChartData/`,
                {
                    init_day: init_day.toISOString().split('T')[0],
                    days_lapse: days_lapse,
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

export default Home;


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
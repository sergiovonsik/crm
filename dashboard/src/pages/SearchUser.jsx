import {useEffect, useState} from "react";
import Sidebar from "../components/Sidebar";
import SelectedUserData from "../components/SelectedUserData";
import AssignmentForm from "../components/AssignmentForm";
import DiscountPassForm from "../components/DiscountPassForm";
import "../styles/SearchUser.css";
import api from "../api.js";


function SearchUser() {
    const [inputValue, setInputValue] = useState("");
    const [usersFound, setUsersFound] = useState([]);
    const [userIsSelected, setUsersIsSelected] = useState(false);
    const [selectedUserData, setSelectedUserData] = useState({});
    const [paymentTickets, setPaymentTickets] = useState([]);
    const [ticketsFilter, setTicketsFilter] = useState(true);
    const [bookingFiles, setBookingFiles] = useState([]);
    const [bookingFilter, setBookingFilter] = useState(true);

    useEffect(() => {
        if (userIsSelected) {
            getUserData();
            console.log(selectedUserData)
        }
    }, [selectedUserData])


    const getUserData = async () => {
        try {
            const res = await api.get(`api/userAdmin/${selectedUserData.pk}/info/`);
            const data = res.data;

            console.log(data);

            let booking_tickets = data.bookings;
            booking_tickets.sort((a, b) => new Date(a.date) - new Date(b.date));
            sessionStorage.setItem("bookingFiles", JSON.stringify(booking_tickets)); // Save to sessionStorage
            setBookingFiles(booking_tickets || []);

            let payment_ticket = data.payment_ticket
            payment_ticket.sort((a, b) => new Date(a.expire_time) - new Date(b.expire_time));
            sessionStorage.setItem("payment_ticket", JSON.stringify(payment_ticket)); // Save to sessionStorage
            setPaymentTickets(payment_ticket || []);


            console.log(data);
        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        await getSearchData(inputValue);
    };

    const getSearchData = async (query) => {
        try {
            const res = await api.get("/api/userAdmin/SearchUsers/", {
                params: { input_value: query },
            });
            const clientsFound = JSON.parse(res.data.clients_found)

            setUsersFound(clientsFound);
        } catch (err) {
            console.error("Error fetching users:", err);
            setUsersFound([]); // En caso de error, asegurarse de que sea un array vacío
        }
    };

    const searchUserMenu = (
    <div>
            <div className="title">Search users:</div>
            <form onSubmit={handleSubmit} className="form-group">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Enter text..."
                    className="p-2 border rounded"
                />
                <button type="submit" className="form-button">
                    Submit
                </button>
            </form>
            {usersFound.length > 0 && (
            <div className="user-list-container">
                    {usersFound.map((user) => (
                        <div key={user.pk}
                             className="user-box"
                             onClick={() =>{
                                 let userDataSerialized = user.fields
                                 userDataSerialized.pk = user.pk;
                                 console.log(userDataSerialized)
                                 setSelectedUserData(userDataSerialized)
                                 setUsersIsSelected(true);
                             }
                             }>
                            {
                                user.fields.last_name && (
                                    <p className="name">
                                        real name: {user.fields.first_name}, {user.fields.last_name}
                                    </p>)
                            }
                            <p className="username">
                                username: {user.fields.username}
                            </p>
                            <p className="username">
                                pk: {user.pk}
                            </p>
                            <p className="email">
                                email: {user.fields.email}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )

    const FoundUserMenu = (
    <div>
        <button className="form-button" onClick={() => {
            setUsersIsSelected(false);
            setSelectedUserData({});
            setUsersFound([]);
        }}>
            Go Back
        </button>

        <div className="inline-elements">
            <div className="inner-container">
                < AssignmentForm selectedUserData={selectedUserData} setSelectedUserData={setSelectedUserData}/>
            </div>
            <div className="inner-container">

                < DiscountPassForm selectedUserData={selectedUserData} setSelectedUserData={setSelectedUserData}/>
            </div>

        </div>

        <div>
            <SelectedUserData
                selectedUserData={selectedUserData}
                paymentTickets={paymentTickets}
                setTicketsFilter={setTicketsFilter}
                ticketsFilter={ticketsFilter}
                bookingFiles={bookingFiles}
                setBookingFilter={setBookingFilter}
                bookingFilter={bookingFilter}
            />
        </div>
    </div>
    )

    return (
        <div>
            <Sidebar />
            <div className="main-content">
                <div>
                    {userIsSelected ? FoundUserMenu : searchUserMenu }
                </div>
            </div>
        </div>
    );
}

export default SearchUser;

import { useState, useEffect } from "react";
import api from "../api";
import Ticket from "../components/Ticket";
import Sidebar from "../components/Sidebar";
import "../styles/Home.css";

function Home() {
    const [paymentTickets, setPaymentTickets] = useState([]);
    const [user , setUser ] = useState({});
    useEffect(() => {
        getUserTickets();
    }, []);

    const getUserTickets = async () => {
        try {
            const res = await api.get(`/api/user/me/info/`);
            const data = res.data;
            const userObjectData = {
                'username': data.username,
                'id': data.id,
                'date_joined': data.date_joined,
                'last_login': data.last_login,
            };
            let payment_ticket = data.payment_ticket

            payment_ticket.sort((a, b) => {
                // 1. Prioritize `expire: false` objects
                if (a.is_expired !== b.is_expired) {
                    return a.is_expired ? 1 : -1;  // `false` first, `true` last
                }
                // 2. If `expire` is the same, sort by `expire_date` (earlier date first)
                return new Date(a.expire_time) - new Date(b.expire_time);
            });

            setPaymentTickets(payment_ticket || []);
            setUser(userObjectData)
            console.log(data.payment_ticket);
        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
                <div className="profile-container">
                    <h2>User Profile</h2>
                    <div className="profile-box">
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>ID:</strong> {user.id}</p>
                        <p><strong>Date Joined:</strong> {user.date_joined}</p>
                        <p><strong>Last Login:</strong> {user.last_login}</p>
                    </div>
                </div>

                <div>
                    <h2>Tickets:</h2>
                    {Array.isArray(paymentTickets) && paymentTickets.length > 0 ? (
                        paymentTickets.map((ticket) => (
                            <Ticket ticket={ticket} key={ticket.id}/>
                        ))
                    ) : (
                        <p>No tickets found.</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Home;


/*

<form onSubmit={createNote}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="content">Content:</label>
                <br />
                <textarea
                    id="content"
                    name="content"
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                ></textarea>
                <br />
                <input type="submit" value="Submit"></input>
            </form>

*/


/*
    const deleteNote = (id) => {
        api
            .delete(`/api/notes/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Note deleted!");
                else alert("Failed to delete note.");
                getUserTickets();
            })
            .catch((error) => alert(error));
    };

    const createNote = (e) => {
        e.preventDefault();
        api
            .post("/api/notes/", { content, title })
            .then((res) => {
                if (res.status === 201) alert("Note created!");
                else alert("Failed to make note.");
                getUserTickets();
            })
            .catch((err) => alert(err));
    };
*/
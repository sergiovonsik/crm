import { useState, useEffect } from "react";
import api from "../api";
import Ticket from "../components/Ticket";
import "../styles/Home.css";

function Home() {
    const [paymentTickets, setPaymentTickets] = useState([]); // ✅ Ensure it's always an array
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");

    useEffect(() => {
        getUserTickets();
    }, []);

    const getUserTickets = async () => {
        try {
            const res = await api.get(`/api/user/me/info`);
            const data = res.data;
            setPaymentTickets(data.payment_ticket || []); // ✅ Ensure it's always an array
            console.log(data.payment_ticket);
        } catch (err) {
            console.error("Error fetching tickets:", err);
            alert("Failed to load tickets.");
        }
    };

    return (
        <div>
            <h1>Profile:</h1>
            <div>
                <h2>Tickets:</h2>
                {Array.isArray(paymentTickets) && paymentTickets.length > 0 ? (
                    paymentTickets.map((ticket) => (
                        <Ticket ticket={ticket} key={ticket.id} />
                    ))
                ) : (
                    <p>No tickets found.</p>
                )}
            </div>
            <h2>Buy more passes</h2>
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
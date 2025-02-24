import { useState } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/AssignPasses.css";
import api from "../api.js";

function AssignPasses() {
    const [activityType, setActivityType] = useState("");
    const [passAmount, setPassAmount] = useState("");
    const [inputValue, setInputValue] = useState("");
    const [usersFound, setUsersFound] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        await getUserData(inputValue);
    };

    const getUserData = async (query) => {
        try {
            const res = await api.get("/api/userAdmin/SearchUsers/", {
                params: { input_value: query },
            });
            const clientsFound = JSON.parse(res.data.clients_found)
            console.log(clientsFound)
            console.log(typeof(clientsFound))

            setUsersFound(clientsFound);
        } catch (err) {
            console.error("Error fetching users:", err);
            setUsersFound([]); // En caso de error, asegurarse de que sea un array vacío
        }
    };

    return (
        <div>
            <Sidebar />
            <div className="main-content">
                <div className="dashboard">
                    <h2>Search users:</h2>
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
                                <div key={user.pk} className="user-box">
                                    {
                                        user.fields.last_name && (
                                        <p className="name">
                                            real name: {user.fields.first_name}, {user.fields.last_name}
                                        </p>)
                                    }
                                    <p className="username">
                                        username: {user.fields.username}
                                    </p>
                                    <p className="email">
                                        email: {user.fields.email}
                                    </p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default AssignPasses;

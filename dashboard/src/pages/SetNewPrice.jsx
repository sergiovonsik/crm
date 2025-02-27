import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/SearchUser.css";
import api from "../api.js";
import PriceForm from "../components/PriceForm.jsx";
import Price from "../components/Price.jsx";
import Ticket from "../components/Ticket.jsx";

function BookingsForToday() {
    const [existingPrices, setExistingPrices] = useState([]);

    useEffect(() => {
        getExistingPrices();
    }, []);

    const getExistingPrices = async () => {
        try {
            const res = await api.get(`api/mercadopago/show_all_prices/`);
            console.log(res.data);
            setExistingPrices(res.data);

        } catch (err) {
            console.error("Error fetching data:", err);
            alert("Failed to load data.");
        }
    };

    const deletePrice = async (priceId) => {
        try {
            const res = await api.delete(`/api/mercadopago/set_price/${(priceId).toString()}/`);
            console.log("Price deleted:", res.data);
            alert("Price deleted successfully!");

            // Opcional: Actualizar la lista de precios después de eliminar uno
            setExistingPrices(res.data.existing_prices);
        } catch (err) {
            console.error("Error deleting price:", err.response);
            alert(err.response?.data?.error || "An unexpected error occurred.");
        }
    };


    const deleteBox = (id) => {
        const userConfirmed = window.confirm("Are you sure you want to close the notification?");
        if (userConfirmed) {
            console.log("Delete confirmed!");
            deletePrice(id)
        }
    }


    return (
        <div>
            <Sidebar />
            <div className="main-content">
                <div>
                    <div>
                        <PriceForm setExistingPrices={setExistingPrices} />
                    </div>

                    <div>
                        {existingPrices.map((data) => (
                            <div onClick={() => deleteBox(data.id)}  key={data.id}>
                                <Price data={data}/>
                            </div>

                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default BookingsForToday;

import { useState, useEffect } from "react";
import "../styles/BuyPasses.css";
import api from "../api.js";
import Sidebar from "../components/Sidebar";
import Price from "../components/Price.jsx";
import LoadingIndicator from "../components/LoadingIndicator.jsx";
import MercadoPagoButton from "../components/MercadoPagoButton.jsx";

function BuyPasses() {
    const [typeOfService, setTypeOfService] = useState('');
    const [passAmount, setPassAmount] = useState('');
    const [price, setPrice] = useState("");
    const [formSelectionData, setFormSelectionData] = useState({});
    const [subscriptionIsSelected, setSubscriptionIsSelected] = useState(false);

    useEffect(() => {
        getPricesData();
    }, []);

    const getPricesData = async () => {
        try {
            const res = await api.get("api/mercadopago/set_price/");
            console.log(res.data);
            setFormSelectionData(res.data.processed_data); // Corregido
        } catch (error) {
            const errorMessage = "Booking failed: " + (error.response?.data?.error || error.message);
            console.log(errorMessage);
        }
    };

    const fillMPButtonData = (data) => {
        setPrice(data.price);
        setTypeOfService(data.type_of_service);
        setPassAmount(data.pass_amount);
        setSubscriptionIsSelected(true);
    };


    return (
        <div>
            <Sidebar />
            <div className="main-content">
                <div className="dashboard">
                    <div className='title'>Select Your Subscription</div>
                    {subscriptionIsSelected && (
                        <div className="summary">
                            <p>
                                You have selected: {passAmount} {typeOfService.replace('_', ' ')} pass for ${price}.
                            </p>
                            {price && (
                                <MercadoPagoButton
                                    key={`${typeOfService}-${passAmount}-${price}`} // Force re-render when these values change
                                    type_of_service={typeOfService}
                                    amount_of_uses={passAmount}
                                    price={price.toString()}
                                />
                            )}
                        </div>
                    )}

                </div>
                <div className="prices-container">
                    <div className="left">
                        <div className="sub-title"> Buy classes</div>
                        {formSelectionData.classes ? (
                            formSelectionData.classes.map((data) => {
                                data.type_of_service = "classes";
                                return (
                                    <div className="child"
                                             key={data.id}
                                             onClick={() => fillMPButtonData(data)}>
                                        <Price data={data}/>
                                    </div>
                                );
                            })
                        ) : (
                            <LoadingIndicator/>
                        )}
                    </div>
                    <div className="right">
                        <div className="sub-title"> Buy free climb passes</div>
                        {formSelectionData.free_climbing ? (
                            formSelectionData.free_climbing.map((data) => {
                                data.type_of_service = "free_climbing";
                                return (
                                    <div className="child"
                                             key={data.id}
                                             onClick={() => fillMPButtonData(data)}>
                                    <Price data={data}/>
                                    </div>
                                );
                            })
                        ) : (
                            <LoadingIndicator/>
                        )}

                    </div>


                </div>
            </div>
        </div>
    );
}

export default BuyPasses;

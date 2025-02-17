import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/BuyPasses.css";
import MercadoPagoButton from "../components/MercadoPagoButton.jsx";

/*const passes = {
    classes:[{amount:4, price:40}, {amount:8, price:80}, {amount:16, price:120}],
    free_climb:[{amount:4, price:40}, {amount:8, price:80}, {amount:16, price:120}]
};*/
function BuyPasses() {
    const [activityType, setActivityType] = useState('');
    const [passAmount, setPassAmount] = useState('');
    const [price, setPrice] = useState(null);


    useEffect(() => {
        handleSelectionChange();
    }, )

    const pricing = {
        classes: { 4: 50, 8: 90, 16: 160 },
        free_climbing: { 4: 60, 8: 110, 16: 200 },
    };

    const handleSelectionChange = () => {
        if (activityType && passAmount) {
            const selectedPrice = pricing[activityType]?.[passAmount] || 0;
            setPrice(selectedPrice);
        } else {
            setPrice(null);
        }
    };

    return (
        <div>
            <Sidebar/>
            <div className="main-content">
                <div className="dashboard">
                    <h2>Select Your Activity</h2>
                    <div className="form-group">
                        <label htmlFor="activityType">Activity Type:</label>
                        <select
                            id="activityType"
                            value={activityType}
                            onChange={(e) => {
                                setActivityType(e.target.value);
                                handleSelectionChange();
                            }}
                        >
                            <option value="">--Select Activity--</option>
                            <option value="classes">Classes</option>
                            <option value="free_climbing">Free Climbing</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="passAmount">Number of Passes:</label>
                        <select
                            id="passAmount"
                            value={passAmount}
                            onChange={(e) => {
                                setPassAmount(e.target.value);
                                handleSelectionChange();
                            }}
                        >
                            <option value="">--Select Passes--</option>
                            <option value="4">4</option>
                            <option value="8">8</option>
                            <option value="16">16</option>
                        </select>
                    </div>
                    {price !== null && (
                        <div className="summary">
                            <p>
                                You have selected {passAmount} {activityType.replace('_', ' ')} pass
                                {passAmount > 1 ? 'es' : ''} for ${price}.
                            </p>
                            <MercadoPagoButton
                                type_of_service={activityType}
                                amount_of_uses={passAmount}
                                price={price.toString()}
                            />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default BuyPasses;


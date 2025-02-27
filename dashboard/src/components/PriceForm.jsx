import "../styles/Form.css";
import api from "../api.js";
import PropTypes from 'prop-types';
import {useForm} from "react-hook-form";
import {useState} from "react";

function PriceForm({setExistingPrices}) {
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm();


    const onSubmit = async (data) => {
        setSuccess(null);
        setError(null);

        data.price = JSON.stringify(Number(data.price));
        data.pass_amount = JSON.stringify(Number(data.pass_amount));

        console.log("Data:", data);

        try {
            const res = await api.post(`api/mercadopago/set_price/`, data);
            console.log("Response:", res.data);
            console.log("Data sent successfully!");
            setExistingPrices(res.data.existing_prices);
            setSuccess("New Price set successfully!");
        } catch (err) {
            console.error("Error sending data:", err.response);
            setError(err.response?.data?.error || "An unexpected error occurred.");
        }
    };


    return (
        <div>
            <div className="title">Assign passes to user:</div>
            <form onSubmit={handleSubmit(onSubmit)}>
                <select {...register("type_of_service", {required: "This field is required"})}>
                    <option value="classes">Classes</option>
                    <option value="free_climbing">Free Climbing</option>
                </select>
                {errors.type_of_service && <p>{errors.type_of_service.message}</p>}

                <input
                    type="number"
                    placeholder="Amount of passes to add"
                    {...register("pass_amount", {
                        required: "This field is required",
                        min: {value: 1, message: "Minimum value is 1"},
                        max: {value: 32, message: "Maximum value is 32"}
                    })}
                />
                {errors.pass_amount && <p>{errors.pass_amount.message}</p>}

                <input
                    type="number"
                    placeholder="Set a price"
                    {...register("price", {
                        required: "This field is required",
                        min: {value: 1, message: "Minimum value is 1"},
                    })}
                />
                {errors.price && <p>{errors.price.message}</p>}

                <input type="submit" value="Submit"/>
            </form>
            {error !== null &&
                <div className="error-message">
                    {error}
                </div>
            }
            {success !== null &&
                <div className="success-message">
                    {success}
                </div>
            }

        </div>
    );
}

PriceForm.propTypes = {
    setErrorInfo: PropTypes.func,
    setExistingPrices: PropTypes.func,
};

export default PriceForm;

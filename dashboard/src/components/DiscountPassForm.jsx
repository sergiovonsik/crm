import "../styles/Form.css";
import {useForm} from "react-hook-form";
import api from "../api.js";
import PropTypes from 'prop-types';
import {useState} from "react";

function DiscountPassForm({ selectedUserData, setSelectedUserData }) {
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const {
        register,
        handleSubmit,
        watch,
        formState: { errors }
    } = useForm();

    // Observar el tipo de servicio seleccionado
    const selectedService = watch("type_of_service", "classes");

    const onSubmit = async (data) => {
        setSuccess(null);
        setError(null);
        console.log("Data:", data);
        data.date = new Date().toISOString().split("T")[0];
        try {
            const res = await api.post(`api/userAdmin/${selectedUserData.pk}/takeAPass/`, data);
            console.log("Response:", res.data);
            console.log("Data sent successfully!");
            let userData = res.data;
            userData.pk = res.data.id;
            setSelectedUserData(userData);
            setSuccess("Booking Ticket created successfully!");
        } catch (err) {
            console.error("Error sending data:", err.response);
            setError(err.response?.data?.error || "An unexpected error occurred.");
        }
    };

    return (
        <div>
            <div className="title">Take a pass for user:</div>
            <form onSubmit={handleSubmit(onSubmit)}>
                {/* Select para el tipo de servicio */}
                <select {...register("type_of_service", { required: "This field is required" })}>
                    <option value="classes">Classes</option>
                    <option value="free_climbing">Free Climbing</option>
                </select>
                {errors.type_of_service && <p>{errors.type_of_service.message}</p>}

                {/* Mostrar select de horario si el servicio es "classes" */}
                {selectedService === "classes" && (
                    <select {...register("hour", { required: "Please select a time slot" })}>
                        <option value="6-8">6 to 8</option>
                        <option value="8-10">8 to 10</option>
                    </select>
                )}
                {errors.hour && <p>{errors.hour.message}</p>}

                <input type="submit" value="Submit" />
            </form>

            {error !== null && <div className="error-message">{error}</div>}
            {success !== null && <div className="success-message">{success}</div>}
        </div>
    );
}

DiscountPassForm.propTypes = {
    selectedUserData: PropTypes.shape({
        username: PropTypes.string,
        date_joined: PropTypes.string,
        pk: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
    setSelectedUserData: PropTypes.func.isRequired,
};

export default DiscountPassForm;

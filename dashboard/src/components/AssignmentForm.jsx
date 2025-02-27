import "../styles/Form.css";
import { useForm } from "react-hook-form";
import api from "../api.js";
import PropTypes from 'prop-types';
import {useState} from "react";

function AssignmentForm({selectedUserData, setSelectedUserData}) {
    const [error, setError] = useState(null);

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm();

    const onSubmit = async (data) => {
        try {
            console.log("Data:", data);
            const res = await api.post(`api/userAdmin/${selectedUserData.pk}/addPasses/`, data)
            console.log("Response:", res.data);
            console.log("Data sent successfully!");
            let userData = res.data
            userData.pk = res.data.id
            setSelectedUserData(userData);




        } catch (err) {
            console.error("Error sending data:", err.response);
            setError(err.response.data.error)
        }
    };

    return (
        <div>
            <div className="title">Assign passes to user:</div>
            <form onSubmit={handleSubmit(onSubmit)}>
                <select {...register("type_of_service", { required: "This field is required" })}>
                    <option value="classes">Classes</option>
                    <option value="free_climbing">Free Climbing</option>
                </select>
                {errors.type_of_service && <p>{errors.type_of_service.message}</p>}

                <input
                    type="number"
                    placeholder="Amount of passes to add"
                    {...register("amount_of_uses", {
                        required: "This field is required",
                        min: { value: 1, message: "Minimum value is 1" },
                        max: { value: 32, message: "Maximum value is 32" }
                    })}
                />
                {errors.amount_of_uses && <p>{errors.amount_of_uses.message}</p>}

                <input type="submit" value="Submit" />
            </form>
            {error !== null &&
                <div className="error-message">
                    {error}
                </div>
            }

        </div>
    );
}

AssignmentForm.propTypes = {
    selectedUserData: PropTypes.shape({
        username: PropTypes.string,
        date_joined: PropTypes.string,
        pk: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
    setSelectedUserData: PropTypes.func.isRequired,  // Added to ensure the function is passed
};

export default AssignmentForm;

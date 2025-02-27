import LoginRegisterForm from "../components/LoginRegisterForm.jsx"
import {apiUrl} from "../api"

function Register() {
    const route =`/api/user/register/`;
    return <LoginRegisterForm route={route} method="register" />
}

export default Register
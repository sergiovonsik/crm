import Form from "../components/Form"
import {apiUrl} from "../api"
function Register() {
    const route =`/api/user/register/`;
    return <Form route={route} method="register" />
}

export default Register
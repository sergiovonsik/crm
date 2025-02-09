import Form from "../components/Form"
import GoogleLoginButton from "../components/GoogleLoginButton"

function Login() {
     return (
    <>
        <Form route="http://127.0.0.1:8000/api/token/" method="login" />
        <GoogleLoginButton/>
    </>
    )
}

export default Login
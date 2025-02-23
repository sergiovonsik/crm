import Form from "../components/Form"
import { useNavigate } from "react-router-dom";
import "../styles/Login.css"

function Login() {
  const navigate = useNavigate();
  const route = `/api/token/`;
  return (
      <>
        <div className="container">
          <p className="register-button" onClick={() => navigate("/register")}>
            Don’t have an account? Register
          </p>
          <div>
            <Form route={route} method="login"/>
          </div>
        </div>
      </>

  )
}

export default Login
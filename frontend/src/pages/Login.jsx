import Form from "../components/Form"
import { useNavigate } from "react-router-dom";
import "../styles/Login.css"

function Login() {
  const navigate = useNavigate();

  return (
      <>
        <div className="container">
          <p className="register-button" onClick={() => navigate("/register")}>
            Don’t have an account? Register
          </p>
          <div>
            <Form route="http://127.0.0.1:8000/api/token/" method="login"/>
          </div>
        </div>
      </>

  )
}

export default Login
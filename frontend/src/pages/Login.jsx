import Form from "../components/Form"
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Login() {
  const handleSubmit = async (googleCredential) => {
    try {
      
      const res = await axios.post("http://127.0.0.1:8000/api/user/AuthGoogle/auth/",
          {credential: googleCredential}
      );

      // Store tokens securely
      localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);

      console.log("Login Successful:", res.data);
    } catch (error) {
      console.error("Google authentication failed:", error);
      alert("Google login failed. Please try again.");
    }
  };
    return (
    <>
        <Form route="http://127.0.0.1:8000/api/token/" method="login" />
        <GoogleLogin
            onSuccess={(credentialResponse) => {
                {
                    console.log(credentialResponse.credential);
                    console.log(jwtDecode(credentialResponse.credential));
                    handleSubmit(credentialResponse.credential)
                }
            }}
            onError={() => console.error("Login failed")}/>
    </>
    )
}

export default Login
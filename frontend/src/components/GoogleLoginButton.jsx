import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";
import {apiUrl} from "../api"


function GoogleLoginButton() {
  const navigate = useNavigate();
  const route =`${apiUrl}/api/user/AuthGoogle/auth/`;


  const handleSubmit = async (googleCredential) => {
    try {
      console.log('googleCredential route = '+route);
      console.log(route);
      const res = await axios.post(route,
          {credential: googleCredential}
      );

      // Store tokens securely
      localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);

      console.log("Login Successful:", res.data);
      navigate("/")

    } catch (error) {
      console.error("Google authentication failed:", error);
      alert("Google login failed. Please try again.");
    }
  };

  return (
      <GoogleLogin
          onSuccess={(credentialResponse) => {
            {
              console.log('credentialResponse.credential');
              console.log(credentialResponse.credential);
              console.log(jwtDecode(credentialResponse.credential));
              console.log('calling handleSubmit...')
              handleSubmit(credentialResponse.credential)
            }
          }}
          onError={() => console.error("Login failed")}/>
  );
}

export default GoogleLoginButton;

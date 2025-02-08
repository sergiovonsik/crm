import GoogleLoginButton from "../components/GoogleLoginButton";
import axios from "axios";

const GoogleLogin = () => {
  const handleGoogleLogin = async (googleCredential) => {
    try {
      const response = await axios.post("http://localhost:8000/api/user/AuthGoogle/auth/", {
        token: googleCredential,
      });

      console.log("Login successful:", response.data);
      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);
    } catch (error) {
      console.error("Google login failed:", error.response ? error.response.data : error);
    }
  };

  return (
      <div>
        <h2>Login</h2>
        <GoogleLoginButton onLoginSuccess={handleGoogleLogin} />
      </div>
  );
};

export default GoogleLogin;
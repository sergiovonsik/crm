import { GoogleLogin } from "@react-oauth/google";

function GoogleLoginButton({onLoginSuccess}) {
  return (
      <GoogleLogin
          onSuccess={(credentialResponse) => {
            console.log("Google token:", credentialResponse.credential);
            console.log("credentialResponse", credentialResponse);
            onLoginSuccess(credentialResponse.credential);
          }}
          onError={() => {
            console.log("Google Login Failed");
          }}
      />
  );
};

export default GoogleLoginButton;

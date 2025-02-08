import React from "react";
import ReactDOM from "react-dom/client";
import { GoogleOAuthProvider } from "@react-oauth/google";
import App from "./App";

const GOOGLE_CLIENT_ID =
    "771272588062-p7p9p0r4r0hefupktgtt4h2vu8rgnutf.apps.googleusercontent.com"; // Replace with your Google Client ID

const root = ReactDOM.createRoot(document.getElementById("root")); // ✅ Correct usage

root.render(
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </GoogleOAuthProvider>
);

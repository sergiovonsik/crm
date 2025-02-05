import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/Home.css";
import MercadoPagoButton from "../components/MercadoPagoButton.jsx";

function BuyPasses() {
  return (
      <div>
        <Sidebar/>
        <div className="main-content">
          <div className="profile-container">
            <h2>Available Passes</h2>
              <div className="profile-box">
                <MercadoPagoButton/>
              </div>
          </div>
        </div>
      </div>
  );
}

export default BuyPasses;


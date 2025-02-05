import { initMercadoPago, Wallet } from '@mercadopago/sdk-react'
initMercadoPago('APP_USR-d69ae28c-5036-428e-9440-6fc15a8cf194');
import { useState, useEffect } from "react";
import api from "../api.js";


function MercadoPagoButton(props) {
  const [init_point , setInit_point ] = useState(null);
  const [id , setId ] = useState(null);
  useEffect(() => {
    getInit_point();
  }, []);

  const getInit_point = async () => {
    try {
      const response = await api.post(`/api/mercadopago/`,
          {'type_of_service':"free_climbing",
                'amount_of_uses':"5"}
      );

      console.log("response.data")
      console.log(response.data.init_point)
      console.log(response.data.id)
      setInit_point(response.data.init_point);
      setId(response.data.id);
    } catch (err) {
      console.error("Error fetching tickets:", err);
      alert("Failed to load tickets.");
    }
  };
  if (init_point === null) {
    return <> Loading...</>
  }
  else{
    return (
        <div id="wallet_container">
          <Wallet initialization={{ preferenceId: id }} customization={{ texts:{ valueProp: 'smart_option'}}} />
        </div>
    );
  }

}

export default MercadoPagoButton

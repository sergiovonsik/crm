import { initMercadoPago, Wallet } from '@mercadopago/sdk-react'
initMercadoPago('APP_USR-d69ae28c-5036-428e-9440-6fc15a8cf194');
import { useState, useEffect } from "react";
import api from "../api.js";
import PropTypes from 'prop-types';


function MercadoPagoButton({type_of_service, price}) {
  const [init_point , setInit_point ] = useState(null);
  const [id , setId ] = useState(null);
  useEffect(() => {
    getInit_point();
  }, []);

  const getInit_point = async () => {
    try {
      const response = await api.post(`/api/mercadopago/pay/`,
          {'type_of_service': type_of_service,
                'price': price
          }
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

MercadoPagoButton.propTypes = {
  type_of_service: PropTypes.string.isRequired,
  price: PropTypes.string.isRequired,
};

export default MercadoPagoButton

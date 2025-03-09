import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";

export let apiUrl;
if (import.meta.env.PROD) {
  apiUrl = import.meta.env.VITE_API_BASE_URL_DEPLOY;
  console.log('Running in production mode in apiUrl=' + import.meta.env.VITE_API_BASE_URL_DEPLOY);
} else {
  //apiUrl = import.meta.env.VITE_API_BASE_URL_LOCAL;
    apiUrl = import.meta.env.VITE_API_BASE_URL_DEPLOY;
    console.log('Running in development mode in apiUrl=' + import.meta.env.VITE_API_BASE_URL_LOCAL);
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || apiUrl,
});

// **INTERCEPTOR DE REQUESTS**
api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
);

// **INTERCEPTOR DE RESPUESTAS PARA REFRESCAR EL TOKEN**
api.interceptors.response.use(
    (response) => response, // Si la respuesta es exitosa, devolverla directamente
    async (error) => {
      const originalRequest = error.config;

      // Si obtenemos un error 401 y no es un reintento
      if (error.response && error.response.status === 401 && !originalRequest._retry) {

        console.log("ACCESS TOKEN Expired, requesting a new one...")

        originalRequest._retry = true; // Marcamos el request para evitar bucles infinitos
        try {
          const refreshToken = localStorage.getItem(REFRESH_TOKEN);
          if (!refreshToken) {
            console.error("No refresh token available. Redirecting to login.");
            localStorage.removeItem(ACCESS_TOKEN);
            localStorage.removeItem(REFRESH_TOKEN);
            window.location.href = "/login"; // Redirigir al login
            return Promise.reject(error);
          }

          // Solicitar un nuevo access token
          const response = await axios.post(`${apiUrl}/api/token/refresh/`, { refresh: refreshToken });
          const newAccessToken = response.data.access;

          // Guardar el nuevo token en localStorage
          localStorage.setItem(ACCESS_TOKEN, newAccessToken);

          console.log("SUCCESS getting the new ACCESS_TOKEN");

          // Reintentar la petición original con el nuevo token
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        } catch (err) {
          console.error("Error refreshing token", err);
          localStorage.removeItem(ACCESS_TOKEN);
          localStorage.removeItem(REFRESH_TOKEN);
          window.location.href = "/login"; // Redirigir al login si falla
        }
      }
      else{
        console.log("ACCESS TOKEN Expired, FAILED requesting a new one...")

        return Promise.reject(error);
      }
    }
);

export default api;

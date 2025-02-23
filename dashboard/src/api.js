import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

//export const apiUrl = "http://127.0.0.1:8000";

export let apiUrl
if (import.meta.env.PROD) {
    apiUrl = import.meta.env.VITE_API_BASE_URL_DEPLOY;
    console.log('Running in production mode in apiUrl=' + import.meta.env.VITE_API_BASE_URL_DEPLOY);
} else {
    // Development-specific code
    apiUrl = import.meta.env.VITE_API_BASE_URL_LOCAL;
    console.log('Running in development mode in apiUrl='+ import.meta.env.VITE_API_BASE_URL_LOCAL);
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


export default api;
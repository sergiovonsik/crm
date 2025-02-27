import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom"
import { useEffect } from 'react';
import Login from "./pages/Login"
import Register from "./pages/Register"
import BusinessData from "./pages/BusinessData.jsx"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import SearchUser from "./pages/SearchUser.jsx";
import BookingsForToday from "./pages/BookingsForToday.jsx";
import SetNewPrice from "./pages/SetNewPrice.jsx";
import api from "./api";

const Logout = () => {
  useEffect(() => {
    const logoutUser = async () => {
      try {
        // Perform the logout API call
        const res = await api.post("api/user/logout/", {});
        console.log(res);
      } catch (error) {
        console.error("Logout failed:", error);
      }

      // Clear localStorage after the logout attempt
      localStorage.clear();
    };

    logoutUser();
  }, []); // Empty dependency array means this runs once on component mount

  return <Navigate to="/login" />;
};

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <BusinessData />
            </ProtectedRoute>
          }
        />
        <Route
            path="/search_user"
            element={
              <ProtectedRoute>
                <SearchUser />
              </ProtectedRoute>
            }
        />
        <Route
            path="/booking_for_today"
            element={
              <ProtectedRoute>
                <BookingsForToday />
              </ProtectedRoute>
            }
        />
        <Route
            path="/set_new_price"
            element={
              <ProtectedRoute>
                <SetNewPrice />
              </ProtectedRoute>
            }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

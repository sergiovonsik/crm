import { Link } from "react-router-dom";
import { useState } from "react";
import "../styles/Sidebar.css";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true); // Sidebar starts open

  return (
      <div className={`sidebar ${isOpen ? "open" : "closed"}`}>
        {/* Toggle Button Inside Sidebar */}
        <button className="toggle-btn" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? "←" : "→"}
        </button>

        {/* Sidebar Content */}
        <div className="sidebar-content">
          <h2>{isOpen ? "Dashboard" : "DB"}</h2>
          <nav>
            <ul>
              <li>
                <Link to="/">{isOpen ? "Home" : "🏠"}</Link>
              </li>
              <li>
                <Link to="/logout">{isOpen ? "Logout" : "🚪"}</Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
  );
};

export default Sidebar;

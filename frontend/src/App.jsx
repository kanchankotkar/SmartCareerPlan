
import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Skills from "./pages/Skills";

function App() {
  const [loggedIn, setLoggedIn] = useState(
    Boolean(localStorage.getItem("access_token"))
  );

  const [currentPage, setCurrentPage] = useState("dashboard");

  const handleLogin = () => {
    setLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setLoggedIn(false);
    setCurrentPage("dashboard");
  };

  if (!loggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div>
      <nav
        style={{
          display: "flex",
          gap: "12px",
          padding: "16px 24px",
          background: "#172554",
          alignItems: "center",
        }}
      >
        <button
          onClick={() => setCurrentPage("dashboard")}
          style={{
            padding: "10px 16px",
            cursor: "pointer",
            fontWeight: currentPage === "dashboard" ? "bold" : "normal",
          }}
        >
          Dashboard
        </button>

        <button
          onClick={() => setCurrentPage("skills")}
          style={{
            padding: "10px 16px",
            cursor: "pointer",
            fontWeight: currentPage === "skills" ? "bold" : "normal",
          }}
        >
          Skills Management
        </button>

        <div style={{ flex: 1 }} />

        <button onClick={handleLogout} style={{ padding: "10px 16px" }}>
          Logout
        </button>
      </nav>

      {currentPage === "dashboard" ? (
        <Dashboard />
      ) : (
        <Skills />
      )}
    </div>
  );
}

export default App;

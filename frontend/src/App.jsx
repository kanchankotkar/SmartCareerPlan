import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function App() {
  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const handleLogin = () => {
    setLoggedIn(true);
  };

  if (loggedIn) {
    return <Dashboard />;
  }

  return <Login onLogin={handleLogin} />;
}

export default App;
import { useState } from "react";
import api from "../api/axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (event) => {
  event.preventDefault();

  setMessage("");
  setError("");

  try {
  const response = await api.post("/accounts/login/", {
    email: email,
    password: password,
  });

  console.log("Login Response:", response.data);

  localStorage.setItem("access_token", response.data.access);
  localStorage.setItem("refresh_token", response.data.refresh);

  setMessage("Login successful!");

  onLogin();

} catch (error) {
  console.error("Login Error:", error);

  if (error.response) {
    setError(
      error.response.data.error ||
      error.response.data.detail ||
      "Invalid email or password"
    );
  } else {
    setError("Unable to connect to server");
  }
}
};

  return (
    <div>
      <h1>Smart Career Platform</h1>

      <h2>Login</h2>

      <form onSubmit={handleLogin}>

        <div>
          <label>Email</label>
          <br />

          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Enter your email"
            autoComplete="email"
            required
          />
        </div>

        <br />

        <div>
          <label>Password</label>
          <br />

          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter your password"
            autoComplete="current-password"
            required
          />
        </div>

        <br />

        <button type="submit">
          Login
        </button>

      </form>

      {message && (
        <p>{message}</p>
      )}

      {error && (
        <p>{error}</p>
      )}

    </div>
  );
}

export default Login;
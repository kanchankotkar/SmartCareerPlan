
import { useState } from "react";
import api from "../api/axios";
import "./Login.css";

function Login({ onLogin, onRegister, onForgotPassword }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!email.trim() || !password) {
      setError("Please enter your email and password.");
      return;
    }

    setLoading(true);

    try {
      const response = await api.post("/accounts/login/", {
        email: email.trim(),
        password,
      });

      const { access, refresh } = response.data;

      if (!access || !refresh) {
        throw new Error("The server did not return valid login tokens.");
      }

      // Use the same storage key as your existing dashboard.
      const storage = rememberMe ? localStorage : sessionStorage;

      storage.setItem("access_token", access);
      storage.setItem("refresh_token", refresh);

      // Clear any previous session from the other storage.
      const otherStorage = rememberMe ? sessionStorage : localStorage;
      otherStorage.removeItem("access_token");
      otherStorage.removeItem("refresh_token");

      setMessage("Login successful! Opening your dashboard...");

      if (typeof onLogin === "function") {
        onLogin();
      }
    } catch (err) {
      console.error("Login Error:", err);

      const data = err.response?.data;

      if (data) {
        setError(
          data.error ||
          data.detail ||
          data.message ||
          "Invalid email or password."
        );
      } else {
        setError(
          err.message ||
          "Unable to connect to the server. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">
      <section className="login-showcase">
        <button
          type="button"
          className="login-brand"
          onClick={() => {
            setEmail("");
            setPassword("");
            setError("");
            setMessage("");
          }}
          aria-label="Smart Career Platform home"
        >
          <span className="brand-logo">S</span>
          <span className="brand-name">
            SmartCareer<span>Platform</span>
            <small>LEARN · BUILD · GROW</small>
          </span>
        </button>

        <div className="showcase-copy">
          <span className="showcase-tag">
            <span className="tag-dot" />
            YOUR NEXT CHAPTER STARTS HERE
          </span>

          <h1>
            Turn your
            <br />
            <span>ambition</span> into
            <br />
            achievement.
          </h1>

          <p>
            Build in-demand skills, discover your strengths,
            and create a career path that feels like yours.
          </p>
        </div>

        <div className="career-art" aria-hidden="true">
          <div className="art-glow" />
          <div className="art-sun" />
          <div className="art-mountain mountain-back" />
          <div className="art-mountain mountain-front" />

          <div className="art-road">
            <div className="road-line" />
          </div>

          <div className="art-flag">
            <span />
            <i />
          </div>

          <div className="floating-card floating-card-top">
            <span className="float-icon">↗</span>
            <span>
              <strong>Keep growing</strong>
              <small>Every step counts</small>
            </span>
          </div>

          <div className="floating-card floating-card-bottom">
            <span className="float-check">✓</span>
            <span>
              <strong>Career in progress</strong>
              <small>Your future is taking shape</small>
            </span>
          </div>

          <div className="art-caption">
            <span>01</span>
            <span>YOUR JOURNEY. YOUR FUTURE.</span>
          </div>
        </div>

        <div className="showcase-footer">
          <span>Designed for your next opportunity.</span>
          <span className="footer-sparkle">✳</span>
        </div>
      </section>

      <section className="login-main">
        <div className="login-mobile-brand">
          <span className="brand-logo">S</span>
          <strong>SmartCareer<span>Platform</span></strong>
        </div>

        <div className="login-card">
          <div className="login-heading">
            <div className="login-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                aria-hidden="true"
              >
                <path d="M12 3 3 8l9 5 9-5-9-5Z" />
                <path d="M7 10.3V15c3.2 2.6 6.8 2.6 10 0v-4.7" />
                <path d="M21 8v6" />
              </svg>
            </div>

            <span className="login-eyebrow">WELCOME BACK</span>
            <h2>Good to see you.</h2>
            <p>Sign in to continue your career journey.</p>
          </div>

          {error && (
            <div className="login-alert error-alert" role="alert">
              <span>!</span>
              <p>{error}</p>
            </div>
          )}

          {message && (
            <div className="login-alert success-alert" role="status">
              <span>✓</span>
              <p>{message}</p>
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div className="login-field">
              <label htmlFor="login-email">Email address</label>

              <div className="input-shell">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.7"
                  aria-hidden="true"
                >
                  <rect x="3" y="5" width="18" height="14" rx="3" />
                  <path d="m4 7 8 6 8-6" />
                </svg>

                <input
                  id="login-email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div className="login-field">
              <label htmlFor="login-password">Password</label>

              <div className="input-shell">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.7"
                  aria-hidden="true"
                >
                  <rect x="4" y="10" width="16" height="11" rx="2.5" />
                  <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                  <path d="M12 14v3" />
                </svg>

                <input
                  id="login-password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                  disabled={loading}
                />

                <button
                  className="password-toggle"
                  type="button"
                  onClick={() => setShowPassword((previous) => !previous)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  aria-pressed={showPassword}
                >
                  {showPassword ? (
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.7"
                      aria-hidden="true"
                    >
                      <path d="M3 3 21 21" />
                      <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
                      <path d="M9.9 5.2A10.8 10.8 0 0 1 12 5c5.5 0 9 7 9 7a15 15 0 0 1-3 3.8" />
                      <path d="M6.2 6.2C4.1 7.7 3 12 3 12s3.5 7 9 7a9.5 9.5 0 0 0 3-.5" />
                    </svg>
                  ) : (
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.7"
                      aria-hidden="true"
                    >
                      <path d="M2.5 12s3.5-7 9.5-7 9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7Z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <div className="login-options">
              <label className="remember-option">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(event) => setRememberMe(event.target.checked)}
                  disabled={loading}
                />
                <span className="custom-checkbox">✓</span>
                Remember me
              </label>

              <button
                type="button"
                className="forgot-link"
                onClick={() => {
                  if (onForgotPassword) {
                    onForgotPassword();
                  } else {
                    setError(
                      "Password recovery is not configured yet. Please contact support or use your existing reset-password page."
                    );
                    setMessage("");
                  }
                }}
              >
                Forgot password?
              </button>
            </div>

            <button
              className="login-submit"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="button-spinner" />
                  Signing you in...
                </>
              ) : (
                <>
                  Sign in to your account
                  <span className="submit-arrow">→</span>
                </>
              )}
            </button>
          </form>

          <div className="login-divider">
            <span />
            <p>YOUR CAREER STARTS WITH ONE STEP</p>
            <span />
          </div>

          <div className="login-benefits">
            <div>
              <span className="benefit-icon purple-benefit">✦</span>
              <span>
                <strong>Know your strengths</strong>
                <small>Track your career readiness</small>
              </span>
            </div>

            <div>
              <span className="benefit-icon blue-benefit">↗</span>
              <span>
                <strong>Grow with purpose</strong>
                <small>Build skills that matter</small>
              </span>
            </div>
          </div>

          {onRegister && (
            <p className="register-prompt">
              New to SmartCareer?{" "}
              <button type="button" onClick={onRegister}>
                Create an account
              </button>
            </p>
          )}
        </div>

        <div className="login-legal">
          <span>© {new Date().getFullYear()} SmartCareerPlatform</span>
          <span>LEARN <i /> BUILD <i /> GROW</span>
        </div>
      </section>
    </main>
  );
}

export default Login;

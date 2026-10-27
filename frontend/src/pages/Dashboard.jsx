import { useEffect, useState } from "react";
import { getDashboard } from "../api/dashboardApi";
import "./Dashboard.css";
import Skills from "./Skills";

function Dashboard({ onLogout }) {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState("dashboard");

  useEffect(() => {
    let isMounted = true;

    const loadDashboard = async () => {
      try {
        const response = await getDashboard();

        console.log("Dashboard Response:", response.data);

        if (isMounted) {
          setDashboard(response.data);
          setError("");
        }
      } catch (err) {
        console.error("Dashboard Error:", err);

        if (isMounted) {
          setError("Unable to load dashboard. Please try again.");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadDashboard();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="dashboard-state">
        <div className="loader" />
        <h2>Preparing your career dashboard...</h2>
        <p>Loading your career insights</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-state">
        <div className="state-icon">!</div>
        <h2>Dashboard unavailable</h2>
        <p>{error}</p>
        <button
          className="primary-button"
          onClick={() => window.location.reload()}
        >
          Try Again
        </button>
      </div>
    );
  }

  const user = dashboard?.user ?? {};
  const readinessData = dashboard?.readiness ?? {};
  const skills = dashboard?.skills ?? {};
  const learning = dashboard?.learning ?? {};

  const readiness = Math.min(
    100,
    Math.max(
      0,
      Number(readinessData.readiness_percentage) || 0
    )
  );

  const requiredSkills =
  Number(readinessData.total_required_skills) || 0;

const matchedSkills =
  Number(readinessData.matched_skills) || 0;

const missingSkills =
  Number(readinessData.missing_skills) || 0;

const totalResources =
  Number(learning.total_resources) || 0;

const startedResources =
  Number(learning.started_resources) || 0;

const completedResources =
  Number(learning.completed_resources) || 0;

const learningProgress = Math.min(
  100,
  Math.max(0, Number(learning.average_progress) || 0)
);

  return (
    <div className="career-app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">S</div>
          <div>
            <h2>SmartCareer</h2>
            <span>PLATFORM</span>
          </div>
        </div>

        <p className="nav-label">WORKSPACE</p>

         <nav className="sidebar-nav" aria-label="Main navigation">
            <a
              href="#overview"
              className={`nav-link ${
                currentPage === "dashboard" ? "active" : ""
              }`}
              onClick={() => setCurrentPage("dashboard")}
            >
              <span className="nav-icon">▦</span>
              Dashboard
            </a>

            <a
              href="#readiness"
              className="nav-link"
              onClick={() => setCurrentPage("dashboard")}
            >
              <span className="nav-icon">◉</span>
              Career Readiness
            </a>

            <a
              href="#skills"
              className={`nav-link ${
                currentPage === "skills" ? "active" : ""
              }`}
              onClick={(event) => {
                event.preventDefault();
                setCurrentPage("skills");
              }}
            >
              <span className="nav-icon">◇</span>
              My Skills
            </a>

            <a
              href="#learning"
              className="nav-link"
              onClick={() => setCurrentPage("dashboard")}
            >
              <span className="nav-icon">▤</span>
              Learning Hub
            </a>
          </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <div className="help-icon">✦</div>
            <h3>Keep growing!</h3>
            <p>
              Small learning steps can make a big career difference.
            </p>
            <a href="#learning">Explore learning →</a>
          </div>

          <div className="sidebar-footer">
            <span className="online-dot" />
            Career journey in progress
          </div>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div>
            <p className="breadcrumb">
                Workspace / {currentPage === "dashboard" ? "Dashboard" : "My Skills"}
            </p>

              <h1>
                {currentPage === "dashboard"
                  ? "Career Dashboard"
                  : "Skills Management"}
              </h1>
          </div>
            
         <div className="topbar-actions">
          <div className="profile-chip">
            <div className="avatar">
              {(user.full_name || user.username || "U")
                .trim()
                .charAt(0)
                .toUpperCase()}
            </div>
            <div className="profile-info">
              <strong>
                {user.full_name || user.username || "Career Explorer"}
              </strong>
              <span>{user.target_role || "Target role not set"}</span>
            </div>
          </div>
          <button
              type="button"
              className="logout-button"
              onClick={onLogout}
            >
              Logout
            </button>
         </div>
        </header>
         
         {currentPage === "dashboard" ? (
          <>
        <section className="welcome-banner">
          <div className="welcome-copy">
            <span className="eyebrow">YOUR CAREER, YOUR FUTURE</span>
            <h2>
              Welcome back,{" "}
              {(user.full_name || user.username || "there")
                .trim()
                .split(/\s+/)[0]}
              !
            </h2>
            <p>
              Understand your strengths, identify skill gaps, and take
              the next step toward your dream career.
            </p>
            <a className="banner-button" href="#readiness">
              View career progress <span>→</span>
            </a>
          </div>

          <div className="welcome-art" aria-hidden="true">
            <div className="art-circle circle-one" />
            <div className="art-circle circle-two" />
            <div className="art-card">
              <span className="art-star">✦</span>
              <strong>{readiness}%</strong>
              <span>Career readiness</span>
              <div className="art-mini-bar">
                <span style={{ width: `${readiness}%` }} />
              </div>
            </div>
          </div>
        </section>

        <section className="section-block">
          <div className="section-heading">
            <div>
              <h2>Performance overview</h2>
              <p>Your current career preparation at a glance.</p>
            </div>
            <span className="live-label">
              <span className="online-dot" />
              Your latest data
            </span>
          </div>

          <div className="stats-grid">
            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-icon purple">◉</span>
                <span className="stat-caption">Overall progress</span>
              </div>
              <div className="stat-value">
                {readiness}<span>%</span>
              </div>
              <div className="progress-track">
                <div
                  className="progress-fill purple-fill"
                  style={{ width: `${readiness}%` }}
                />
              </div>
              <p className="stat-foot">Career readiness score</p>
            </article>

            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-icon green">✓</span>
                <span className="stat-caption">Skills acquired</span>
              </div>
              <div className="stat-value">
                {matchedSkills}
                <span className="stat-unit"> skills</span>
              </div>
              <div className="stat-note">
                Out of {requiredSkills} required skills
              </div>
              <p className="stat-foot">Skills matching your target role</p>
            </article>

            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-icon orange">⌁</span>
                <span className="stat-caption">Skill gaps</span>
              </div>
              <div className="stat-value">{missingSkills}</div>
              <div className="stat-note">
                {missingSkills === 0
                  ? "No missing skills reported"
                  : "Areas to focus on next"}
              </div>
              <p className="stat-foot">Opportunities to improve</p>
            </article>

            <article className="stat-card">
              <div className="stat-top">
                <span className="stat-icon blue">▤</span>
                <span className="stat-caption">Learning resources</span>
              </div>
              <div className="stat-value">{totalResources}</div>
              <div className="stat-note">
                {completedResources} completed
              </div>
              <p className="stat-foot">Resources available to you</p>
            </article>
          </div>
        </section>

        <div className="insights-grid">
          <section className="panel readiness-panel" id="readiness">
            <div className="panel-heading">
              <div>
                <h2>Career readiness</h2>
                <p>How prepared are you for your target role?</p>
              </div>
              <span className="panel-symbol">↗</span>
            </div>

            <div className="readiness-content">
              <div
                className="readiness-ring"
                style={{
                  background: `conic-gradient(#7058e8 ${readiness}%, #edf0f6 ${readiness}% 100%)`,
                }}
                role="img"
                aria-label={`Career readiness ${readiness}%`}
              >
                <div className="ring-inner">
                  <strong>{readiness}%</strong>
                  <span>Ready</span>
                </div>
              </div>

              <div className="readiness-details">
                <span className="detail-label">YOUR TARGET ROLE</span>
                <h3>{user.target_role || "Not set yet"}</h3>
                <p>
                  {readiness >= 80
                    ? "Great progress! Keep practising and strengthening your skills."
                    : readiness >= 50
                    ? "You're making progress. Focus on your remaining skill gaps."
                    : "Build your foundation by learning the skills required for your target role."}
                </p>
                <div className="mini-metrics">
                  <div>
                    <strong>{matchedSkills}</strong>
                    <span>Matched</span>
                  </div>
                  <div>
                    <strong>{missingSkills}</strong>
                    <span>Missing</span>
                  </div>
                  <div>
                    <strong>{requiredSkills}</strong>
                    <span>Required</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="panel learning-panel" id="learning">
            <div className="panel-heading">
              <div>
                <h2>Learning progress</h2>
                <p>Stay consistent with your learning goals.</p>
              </div>
              <span className="panel-symbol">✦</span>
            </div>

            <div className="learning-summary">
              <div>
                <span className="detail-label">COMPLETION RATE</span>
                <h3>{Math.round(learningProgress)}%</h3>
              </div>
              <div className="learning-icon">▤</div>
            </div>

            <div className="progress-track learning-track">
              <div
                className="progress-fill blue-fill"
                style={{ width: `${learningProgress}%` }}
              />
            </div>

            <div className="learning-counts">
              <div>
                <span>Completed resources</span>
                <strong>{completedResources}</strong>
              </div>
              <div>
                <span>Total resources</span>
                <strong>{totalResources}</strong>
              </div>
              <div>
                <span>Remaining</span>
                <strong>
                  {Math.max(0, totalResources - completedResources)}
                </strong>
              </div>
            </div>

            <a className="text-link" href="#skills">
              Review your skills <span>→</span>
            </a>
          </section>
        </div>

        <section className="panel skills-panel" id="skills">
          <div className="panel-heading">
            <div>
              <h2>Skills snapshot</h2>
              <p>A quick view of your skills against your career goals.</p>
            </div>
            <span className="skills-badge">
              {requiredSkills} required
            </span>
          </div>

          <div className="skill-summary-grid">
            <div className="skill-summary-item">
              <span className="skill-dot dot-green" />
              <div>
                <strong>Matched skills</strong>
                <p>Skills aligned with your target role</p>
              </div>
              <b>{matchedSkills}</b>
            </div>

            <div className="skill-summary-item">
              <span className="skill-dot dot-orange" />
              <div>
                <strong>Skills to develop</strong>
                <p>Areas that need more attention</p>
              </div>
              <b>{missingSkills}</b>
            </div>
          </div>

          <div className="skills-footer">
            <span>
              <span className="online-dot" />
              Based on your current dashboard data
            </span>
            <span>{requiredSkills} required skills tracked</span>
          </div>
        </section>

        <footer className="dashboard-footer">
          <span>SmartCareerPlatform</span>
          <span>Build skills. Track progress. Grow your career.</span>
        </footer>
          </>
          ) : (
            <Skills />
          )}
      </main>
    </div>
  );
}

export default Dashboard;

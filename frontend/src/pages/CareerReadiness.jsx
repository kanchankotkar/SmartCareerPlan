
function CareerReadiness({ dashboard }) {
  const user = dashboard?.user ?? {};
  const readinessData = dashboard?.readiness ?? {};
  const skills = dashboard?.skills ?? {};

  const matchedSkills = skills.matched ?? [];
  const missingSkills = skills.missing ?? [];

  const readiness = Math.min(
    100,
    Math.max(
      0,
      Number(readinessData.readiness_percentage) || 0
    )
  );

  const nextSteps = [
    ...missingSkills.map((skill) => ({
      skill,
      description: `Learn the fundamentals of ${skill} and practise with a small project.`,
    })),
  ];

  return (
    <div className="readiness-page">
      <section className="readiness-hero">
        <span className="readiness-eyebrow">
          YOUR PERSONAL CAREER PLAN
        </span>

        <h2>Career Readiness</h2>

        <p>
          Track how your current skills match the requirements
          for your target role.
        </p>

        <div className="readiness-role">
          Target role: <strong>{user.target_role || "Not selected"}</strong>
        </div>
      </section>

      <section className="readiness-overview">
        <article className="readiness-score-card">
          <div
            className="readiness-score-ring"
            style={{
              background: `conic-gradient(#7058e8 ${readiness}%, #e9e7f5 ${readiness}% 100%)`,
            }}
          >
            <div className="readiness-score-inner">
              <strong>{readiness}%</strong>
              <span>Ready</span>
            </div>
          </div>

          <div>
            <h3>Your readiness score</h3>
            <p>
              {readiness >= 80
                ? "Excellent progress! Keep strengthening your skills."
                : readiness >= 50
                ? "You're making progress. Focus on your remaining skill gaps."
                : "Start with your missing skills and build your foundation step by step."}
            </p>
          </div>
        </article>

        <article className="readiness-stat-card matched-stat">
          <span>✓</span>
          <p>Matched skills</p>
          <strong>{matchedSkills.length}</strong>
          <small>Skills you already have</small>
        </article>

        <article className="readiness-stat-card missing-stat">
          <span>↗</span>
          <p>Skills to develop</p>
          <strong>{missingSkills.length}</strong>
          <small>Skills required for your role</small>
        </article>

        <article className="readiness-stat-card required-stat">
          <span>◎</span>
          <p>Required skills</p>
          <strong>
            {Number(readinessData.total_required_skills) || 0}
          </strong>
          <small>Skills tracked for your target role</small>
        </article>
      </section>

      <section className="readiness-panel">
        <div className="readiness-section-heading">
          <div>
            <h3>Your skill match</h3>
            <p>See which skills are already in your profile.</p>
          </div>
        </div>

        {matchedSkills.length === 0 ? (
          <p className="readiness-empty">
            No matching skills yet. Add your existing skills
            from My Skills to update your readiness score.
          </p>
        ) : (
          <div className="readiness-skill-list">
            {matchedSkills.map((skill) => (
              <div className="readiness-skill-item" key={skill}>
                <span className="readiness-skill-check">✓</span>
                <strong>{skill}</strong>
                <span className="readiness-status matched-label">
                  Matched
                </span>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="readiness-panel">
        <div className="readiness-section-heading">
          <div>
            <h3>Skills to develop</h3>
            <p>Prioritize these areas to improve your readiness.</p>
          </div>
          <span className="readiness-count">
            {missingSkills.length} remaining
          </span>
        </div>

        {missingSkills.length === 0 ? (
          <p className="readiness-empty">
            Great work! Your current skills cover all the required
            skills tracked for this role.
          </p>
        ) : (
          <div className="readiness-skill-list">
            {nextSteps.map((step) => (
              <div className="readiness-missing-item" key={step.skill}>
                <div className="missing-skill-icon">↗</div>

                <div className="missing-skill-content">
                  <strong>{step.skill}</strong>
                  <p>{step.description}</p>
                </div>

                <span className="readiness-status missing-label">
                  To learn
                </span>
              </div>
            ))}
          </div>
        )}
      </section>

      <div className="readiness-note">
        <strong>How is this score calculated?</strong>
        <p>
          Readiness equals matched required skills divided by
          total required skills, multiplied by 100. Your score
          updates when your skills data changes and the dashboard
          is refreshed.
        </p>
      </div>
    </div>
  );
}

export default CareerReadiness;

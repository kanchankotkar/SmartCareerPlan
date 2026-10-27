
import { useEffect, useState } from "react";
import {
  getLearningRoadmap,
  getLearningProgress,
  updateLearningProgress,
} from "../api/learningApi";
import "./LearningHub.css";

function LearningHub() {
  const [roadmap, setRoadmap] = useState([]);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [savingId, setSavingId] = useState(null);

  useEffect(() => {
    let active = true;

    async function loadLearningData() {
      try {
        const [roadmapResponse, progressResponse] =
          await Promise.all([
            getLearningRoadmap(),
            getLearningProgress(),
          ]);

        if (!active) return;

        setRoadmap(
          roadmapResponse.data.learning_roadmap || []
        );

        const savedProgress = {};

        progressResponse.data.forEach((item) => {
          savedProgress[item.resource] = Number(
            item.progress_percentage || 0
          );
        });

        setProgress(savedProgress);
      } catch (err) {
        if (active) {
          setError(
            err.response?.data?.error ||
              "Unable to load learning resources."
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadLearningData();

    return () => {
      active = false;
    };
  }, []);

  async function saveProgress(resourceId, percentage) {
    setSavingId(resourceId);
    setError("");

    try {
      await updateLearningProgress(resourceId, percentage);

      setProgress((previous) => ({
        ...previous,
        [resourceId]: percentage,
      }));
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to save learning progress."
      );
    } finally {
      setSavingId(null);
    }
  }

  if (loading) {
    return (
      <div className="learning-page">
        <p>Loading your learning roadmap...</p>
      </div>
    );
  }

  return (
    <div className="learning-page">
      <section className="learning-heading">
        <div>
          <p className="learning-eyebrow">
            PERSONALIZED DEVELOPMENT
          </p>
          <h2>Learning Hub</h2>
          <p>
            Learn the skills you need for your target career.
          </p>
        </div>

        <div className="learning-count">
          <strong>{roadmap.length}</strong>
          <span>Skills to improve</span>
        </div>
      </section>

      {error && (
        <div className="learning-error" role="alert">
          {error}
        </div>
      )}

      {roadmap.length === 0 ? (
        <section className="learning-empty">
          <h3>Your roadmap is clear!</h3>
          <p>
            No skill gaps were found for your selected role.
            Keep practicing to maintain your readiness.
          </p>
        </section>
      ) : (
        roadmap.map((item) => (
          <section
            className="learning-skill-section"
            key={item.skill_id}
          >
            <div className="learning-skill-heading">
              <div>
                <h3>{item.skill_name}</h3>
                <p>
                  {item.reason === "Missing"
                    ? "This skill is missing from your profile."
                    : `Current level: ${
                        item.current_level || "Beginner"
                      }`}
                </p>
              </div>

              <span className="required-level">
                Target: {item.required_level || "Beginner"}
              </span>
            </div>

            {item.resources.length === 0 ? (
              <p className="no-resources">
                No resources are available for this skill yet.
              </p>
            ) : (
              <div className="learning-resource-grid">
                {item.resources.map((resource) => {
                  const currentProgress =
                    progress[resource.resource_id] || 0;

                  return (
                    <article
                      className="learning-resource-card"
                      key={resource.resource_id}
                    >
                      <div className="resource-meta">
                        <span>
                          {resource.resource_type || "Resource"}
                        </span>
                        <span>
                          {resource.difficulty || "All levels"}
                        </span>
                      </div>

                      <h4>{resource.title}</h4>

                      <p className="resource-description">
                        {resource.description ||
                          "Build your knowledge with this resource."}
                      </p>

                      <p className="resource-hours">
                        Estimated time:{" "}
                        {resource.estimated_hours != null
                          ? `${resource.estimated_hours} hours`
                          : "Not specified"}
                      </p>

                      <div className="resource-progress">
                        <div className="progress-label">
                          <span>Your progress</span>
                          <strong>{currentProgress}%</strong>
                        </div>

                        <div className="progress-track">
                          <div
                            className="progress-fill"
                            style={{
                              width: `${Math.min(
                                100,
                                Math.max(0, currentProgress)
                              )}%`,
                            }}
                          />
                        </div>
                      </div>

                      <label className="progress-select-label">
                        Update progress
                        <select
                          value={currentProgress}
                          disabled={
                            savingId === resource.resource_id
                          }
                          onChange={(event) =>
                            saveProgress(
                              resource.resource_id,
                              Number(event.target.value)
                            )
                          }
                        >
                          <option value={0}>Not started — 0%</option>
                          <option value={25}>Started — 25%</option>
                          <option value={50}>In progress — 50%</option>
                          <option value={75}>Almost done — 75%</option>
                          <option value={100}>Completed — 100%</option>
                        </select>
                      </label>

                      {resource.resource_url ? (
                        <a
                          className="resource-link"
                          href={resource.resource_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          onClick={() => {
                            if (currentProgress === 0) {
                              saveProgress(
                                resource.resource_id,
                                25
                              );
                            }
                          }}
                        >
                          {currentProgress === 100
                            ? "Review resource"
                            : "Start learning"}
                          <span aria-hidden="true"> ↗</span>
                        </a>
                      ) : (
                        <p className="no-resource-link">
                          A learning link is not available.
                        </p>
                      )}
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        ))
      )}
    </div>
  );
}

export default LearningHub;

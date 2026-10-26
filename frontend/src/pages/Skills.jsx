
import { useEffect, useState } from "react";
import {
  getAllSkills,
  getMySkills,
  addUserSkill,
  updateUserSkill,
  deleteUserSkill,
} from "../api/skillsApi";

import "./Skills.css";

const emptyForm = {
  skill: "",
  skill_level: "Beginner",
  years_experience: "0",
};

function Skills() {
  const [availableSkills, setAvailableSkills] = useState([]);
  const [mySkills, setMySkills] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadSkills = async () => {
    setLoading(true);
    setError("");

    try {
      const [availableResponse, myResponse] = await Promise.all([
        getAllSkills(),
        getMySkills(),
      ]);

      setAvailableSkills(availableResponse.data);
      setMySkills(myResponse.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Could not load skills. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSkills();
  }, []);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    const payload = {
      skill: Number(form.skill),
      skill_level: form.skill_level,
      years_experience: Number(form.years_experience),
    };

    try {
      if (editingId !== null) {
        await updateUserSkill(editingId, {
          skill_level: payload.skill_level,
          years_experience: payload.years_experience,
        });
        setMessage("Skill updated successfully.");
      } else {
        await addUserSkill(payload);
        setMessage("Skill added successfully.");
      }

      resetForm();
      await loadSkills();
    } catch (err) {
      const data = err.response?.data;
      setError(
        data?.error ||
          data?.detail ||
          (typeof data === "object"
            ? Object.values(data || {}).flat().join(" ")
            : "") ||
          "Could not save skill. Please try again."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (item) => {
    setEditingId(item.user_skill_id);
    setForm({
      skill: String(item.skill_id),
      skill_level: item.skill_level,
      years_experience: String(item.years_experience ?? 0),
    });
    setError("");
    setMessage("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDelete = async (item) => {
    const confirmed = window.confirm(
      `Are you sure you want to remove ${item.skill_name} from your skills?`
    );

    if (!confirmed) return;

    setError("");
    setMessage("");

    try {
      await deleteUserSkill(item.user_skill_id);
      setMySkills((previous) =>
        previous.filter(
          (skill) => skill.user_skill_id !== item.user_skill_id
        )
      );
      setMessage(`${item.skill_name} deleted successfully.`);

      if (editingId === item.user_skill_id) {
        resetForm();
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
          err.response?.data?.detail ||
          "Could not delete skill."
      );
    }
  };

  if (loading) {
    return <div className="skills-page"><p>Loading skills...</p></div>;
  }

  return (
    <main className="skills-page">
      <header className="skills-header">
        <div>
          <p className="skills-eyebrow">CAREER DEVELOPMENT</p>
          <h1>Skills Management</h1>
          <p>Manage your skills and track your experience.</p>
        </div>

        <button className="skills-refresh" onClick={loadSkills}>
          Refresh
        </button>
      </header>

      {error && <div className="skills-alert error">{error}</div>}
      {message && <div className="skills-alert success">{message}</div>}

      <section className="skills-card">
        <h2>{editingId !== null ? "Edit Skill" : "Add a New Skill"}</h2>

        <form onSubmit={handleSubmit} className="skills-form">
          <label>
            Skill
            <select
              name="skill"
              value={form.skill}
              onChange={handleChange}
              required
              disabled={editingId !== null}
            >
              <option value="">Select a skill</option>
              {availableSkills.map((skill) => (
                <option
                  key={skill.skill_id}
                  value={skill.skill_id}
                  disabled={mySkills.some(
                    (item) => item.skill_id === skill.skill_id
                  )}
                >
                  {skill.skill_name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Skill Level
            <select
              name="skill_level"
              value={form.skill_level}
              onChange={handleChange}
              required
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </label>

          <label>
            Years of Experience
            <input
              type="number"
              name="years_experience"
              min="0"
              max="60"
              step="0.1"
              value={form.years_experience}
              onChange={handleChange}
              required
            />
          </label>

          <div className="skills-form-actions">
            <button type="submit" disabled={saving}>
              {saving
                ? "Saving..."
                : editingId !== null
                  ? "Update Skill"
                  : "Add Skill"}
            </button>

            {editingId !== null && (
              <button
                type="button"
                className="skills-cancel"
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="skills-card">
        <div className="skills-list-header">
          <div>
            <h2>My Skills</h2>
            <p>Skills saved in your profile: {mySkills.length}</p>
          </div>
        </div>

        {mySkills.length === 0 ? (
          <p className="skills-empty">
            No skills added yet. Use the form above to add your first skill.
          </p>
        ) : (
          <div className="skills-table-wrapper">
            <table className="skills-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Category</th>
                  <th>Level</th>
                  <th>Experience</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {mySkills.map((item) => (
                  <tr key={item.user_skill_id}>
                    <td>{item.skill_name}</td>
                    <td>{item.category || "—"}</td>
                    <td>
                      <span className="skill-level">
                        {item.skill_level}
                      </span>
                    </td>
                    <td>{item.years_experience} years</td>
                    <td>
                      <div className="skills-row-actions">
                        <button
                          type="button"
                          onClick={() => handleEdit(item)}
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          className="skills-delete"
                          onClick={() => handleDelete(item)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}

export default Skills;

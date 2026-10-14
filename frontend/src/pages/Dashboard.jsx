import { useEffect, useState } from "react";
import { getDashboard } from "../api/dashboardApi";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await getDashboard();

      console.log("Dashboard Response:", response.data);

      setDashboard(response.data);
    } catch (error) {
      console.error("Dashboard Error:", error);

      setError("Unable to load dashboard");
    }
  };

  if (error) {
    return <h2>{error}</h2>;
  }

  if (!dashboard) {
    return <h2>Loading dashboard...</h2>;
  }


  useEffect(() => {
    getDashboard()
        .then((response) => {
            console.log("Dashboard Data:", response.data);
        })
        .catch((error) => {
            console.log("Dashboard Error:", error);
        });
}, []);
  return (
    <div>
      <h1>Smart Career Platform</h1>

      <h2>Dashboard</h2>

      <hr />

      <h3>Career Readiness</h3>

      <p>
        Target Role: {dashboard.target_role}
      </p>

      <p>
        Readiness: {dashboard.readiness_percentage}%
      </p>

      <hr />

      <h3>Overview</h3>

      <p>
        Total Required Skills: {dashboard.total_required_skills}
      </p>

      <p>
        Matched Skills: {dashboard.matched_skills}
      </p>

      <p>
        Missing Skills: {dashboard.missing_skills}
      </p>

      <p>
        Total Learning Resources: {dashboard.total_learning_resources}
      </p>

      <p>
        Completed Resources: {dashboard.completed_resources}
      </p>

    </div>
  );
}

export default Dashboard;
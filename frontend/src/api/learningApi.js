import api from "./axios";

// Get a personalized roadmap for a job role
export const getLearningRoadmap = (roleId) => {
  return api.post("/learning/roadmap/", {
    role_id: roleId,
  });
};

// Get the logged-in user's learning progress
export const getLearningProgress = () => {
  return api.get("/learning/progress/");
};

// Save or update progress for a resource
export const updateLearningProgress = (
  resourceId,
  progressPercentage
) => {
  return api.post("/learning/progress/", {
    resource_id: resourceId,
    progress_percentage: progressPercentage,
  });
};
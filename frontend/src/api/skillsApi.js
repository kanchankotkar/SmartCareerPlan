
import api from "./axios";

// Get all available skills
export const getAllSkills = () => {
  return api.get("/skills/");
};

// Get skills belonging to the logged-in user
export const getMySkills = () => {
  return api.get("/skills/user/my/");
};

// Add a skill to the user's profile
export const addUserSkill = (data) => {
  return api.post("/skills/user/", data);
};

// Update a user's skill
export const updateUserSkill = (userSkillId, data) => {
  return api.patch(`/skills/user/${userSkillId}/`, data);
};

// Delete a user's skill
export const deleteUserSkill = (userSkillId) => {
  return api.delete(`/skills/user/${userSkillId}/`);
};

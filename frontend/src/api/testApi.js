import api from "./axios";

export const getSkills = () => {
  return api.get("/skills/");
};
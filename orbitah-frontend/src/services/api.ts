import type {
  Achievement,
  ExplorationState,
  FocusSession,
  Goal,
  Group,
  Token,
  User,
  UserCreate,
  UserLogin,
  UserUpdate,
} from "@/types/api";
import type { AxiosInstance, AxiosResponse } from "axios";
import axios from "axios";

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8001", // Use env var or default to dev
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      // Redirect to login or show auth error
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (userData: UserCreate): Promise<User> => {
    const response: AxiosResponse<User> = await api.post(
      "/auth/register",
      userData
    );
    return response.data;
  },

  login: async (credentials: UserLogin): Promise<Token> => {
    const response: AxiosResponse<Token> = await api.post(
      "/auth/login",
      credentials
    );
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response: AxiosResponse<User> = await api.get("/auth/me");
    return response.data;
  },
};

// Users API
export const usersAPI = {
  getUsers: async (skip: number = 0, limit: number = 100): Promise<User[]> => {
    const response: AxiosResponse<User[]> = await api.get("/users", {
      params: { skip, limit },
    });
    return response.data;
  },

  getUser: async (userId: string): Promise<User> => {
    const response: AxiosResponse<User> = await api.get(`/users/${userId}`);
    return response.data;
  },

  updateUser: async (userId: string, userData: UserUpdate): Promise<User> => {
    const response: AxiosResponse<User> = await api.put(
      `/users/${userId}`,
      userData
    );
    return response.data;
  },

  deleteUser: async (userId: string): Promise<User> => {
    const response: AxiosResponse<User> = await api.delete(`/users/${userId}`);
    return response.data;
  },
};

// Groups API
export const groupsAPI = {
  getGroups: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<Group[]> => {
    const response: AxiosResponse<Group[]> = await api.get("/groups", {
      params: { skip, limit },
    });
    return response.data;
  },

  getGroup: async (groupId: string): Promise<Group> => {
    const response: AxiosResponse<Group> = await api.get(`/groups/${groupId}`);
    return response.data;
  },

  createGroup: async (
    groupData: Omit<Group, "id" | "members" | "shared_goals">
  ): Promise<Group> => {
    const response: AxiosResponse<Group> = await api.post("/groups", groupData);
    return response.data;
  },

  updateGroup: async (
    groupId: string,
    groupData: Partial<Group>
  ): Promise<Group> => {
    const response: AxiosResponse<Group> = await api.put(
      `/groups/${groupId}`,
      groupData
    );
    return response.data;
  },

  deleteGroup: async (groupId: string): Promise<Group> => {
    const response: AxiosResponse<Group> = await api.delete(
      `/groups/${groupId}`
    );
    return response.data;
  },
};

// Goals API
export const goalsAPI = {
  getGoals: async (skip: number = 0, limit: number = 100): Promise<Goal[]> => {
    const response: AxiosResponse<Goal[]> = await api.get("/goals", {
      params: { skip, limit },
    });
    return response.data;
  },

  getGoal: async (goalId: string): Promise<Goal> => {
    const response: AxiosResponse<Goal> = await api.get(`/goals/${goalId}`);
    return response.data;
  },

  createGoal: async (goalData: Omit<Goal, "id">): Promise<Goal> => {
    const response: AxiosResponse<Goal> = await api.post("/goals", goalData);
    return response.data;
  },

  updateGoal: async (
    goalId: string,
    goalData: Partial<Goal>
  ): Promise<Goal> => {
    const response: AxiosResponse<Goal> = await api.put(
      `/goals/${goalId}`,
      goalData
    );
    return response.data;
  },

  deleteGoal: async (goalId: string): Promise<Goal> => {
    const response: AxiosResponse<Goal> = await api.delete(`/goals/${goalId}`);
    return response.data;
  },
};

// Focus Sessions API
export const focusSessionsAPI = {
  getFocusSessions: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<FocusSession[]> => {
    const response: AxiosResponse<FocusSession[]> = await api.get(
      "/focus-sessions",
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  getFocusSession: async (sessionId: string): Promise<FocusSession> => {
    const response: AxiosResponse<FocusSession> = await api.get(
      `/focus-sessions/${sessionId}`
    );
    return response.data;
  },

  createFocusSession: async (
    sessionData: Omit<FocusSession, "id">
  ): Promise<FocusSession> => {
    const response: AxiosResponse<FocusSession> = await api.post(
      "/focus-sessions",
      sessionData
    );
    return response.data;
  },

  updateFocusSession: async (
    sessionId: string,
    sessionData: Partial<FocusSession>
  ): Promise<FocusSession> => {
    const response: AxiosResponse<FocusSession> = await api.put(
      `/focus-sessions/${sessionId}`,
      sessionData
    );
    return response.data;
  },

  deleteFocusSession: async (sessionId: string): Promise<FocusSession> => {
    const response: AxiosResponse<FocusSession> = await api.delete(
      `/focus-sessions/${sessionId}`
    );
    return response.data;
  },
};

// Achievements API
export const achievementsAPI = {
  getAchievements: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<Achievement[]> => {
    const response: AxiosResponse<Achievement[]> = await api.get(
      "/achievements",
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  getAchievement: async (achievementId: string): Promise<Achievement> => {
    const response: AxiosResponse<Achievement> = await api.get(
      `/achievements/${achievementId}`
    );
    return response.data;
  },
};

// Exploration API
export const explorationAPI = {
  getExplorationState: async (userId: string): Promise<ExplorationState> => {
    const response: AxiosResponse<ExplorationState> = await api.get(
      `/exploration/${userId}`
    );
    return response.data;
  },

  updateExplorationState: async (
    userId: string,
    stateData: Partial<ExplorationState>
  ): Promise<ExplorationState> => {
    const response: AxiosResponse<ExplorationState> = await api.put(
      `/exploration/${userId}`,
      stateData
    );
    return response.data;
  },
};

export default api;

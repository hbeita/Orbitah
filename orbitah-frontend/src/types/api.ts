export interface User {
  id: string;
  username: string;
  email: string;
  avatar_url?: string;
  routine_description?: string;
  available_time?: string;
  focus_preference?: string;
  group_id?: string;
  current_location?: string;
  experience_points?: number;
  rank?: string;
  streak_days?: number;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  avatar_url?: string;
  routine_description?: string;
  available_time?: string;
  focus_preference?: string;
  group_id?: string;
  current_location?: string;
  experience_points?: number;
  rank?: string;
  streak_days?: number;
}

export interface UserUpdate {
  username?: string;
  email?: string;
  avatar_url?: string;
  routine_description?: string;
  available_time?: string;
  focus_preference?: string;
  group_id?: string;
  current_location?: string;
  experience_points?: number;
  rank?: string;
  streak_days?: number;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface Group {
  id: string;
  name: string;
  code: string;
  ship_type?: string;
  motto?: string;
  progress?: number;
  members: string[];
  shared_goals: string[];
}

export interface Goal {
  id: string;
  title: string;
  description?: string;
  type: string;
  status: string;
  creator_id: string;
  category?: string;
  created_by_ai?: boolean;
  created_at?: string;
  due_date?: string;
  rewards_xp?: number;
  rewards_custom_reward?: string;
  rewards_unlock?: string;
  group_id?: string;
  assigned_user_ids: string[];
}

export interface FocusSession {
  id: string;
  user_id: string;
  method: string;
  started_at: string;
  duration: number;
  goal_id?: string;
}

export interface Achievement {
  id: string;
  code: string;
  name: string;
  description?: string;
  icon?: string;
  xp_reward?: number;
}

export interface ExplorationState {
  user_id: string;
  unlocked_locations: string[];
  current_location?: string;
  lore_progress?: string;
  achievements: string[];
}

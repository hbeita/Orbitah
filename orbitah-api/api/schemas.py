from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None
    routine_description: Optional[str] = None
    available_time: Optional[str] = None
    focus_preference: Optional[str] = None
    group_id: Optional[str] = None
    current_location: Optional[str] = None
    experience_points: Optional[int] = 0
    rank: Optional[str] = None
    streak_days: Optional[int] = 0

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    routine_description: Optional[str] = None
    available_time: Optional[str] = None
    focus_preference: Optional[str] = None
    group_id: Optional[str] = None
    current_location: Optional[str] = None
    experience_points: Optional[int] = None
    rank: Optional[str] = None
    streak_days: Optional[int] = None

class User(UserBase):
    id: str
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None
    routine_description: Optional[str] = None
    available_time: Optional[str] = None
    focus_preference: Optional[str] = None
    group_id: Optional[str] = None
    current_location: Optional[str] = None
    experience_points: Optional[int] = 0
    rank: Optional[str] = None
    streak_days: Optional[int] = 0
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    email: Optional[str] = None

class GroupBase(BaseModel):
    name: str
    code: str
    ship_type: Optional[str] = None
    motto: Optional[str] = None
    progress: Optional[float] = 0.0

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    ship_type: Optional[str] = None
    motto: Optional[str] = None
    progress: Optional[float] = None

class Group(GroupBase):
    id: str
    members: List[str] = []
    shared_goals: List[str] = []
    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str
    status: str
    creator_id: str
    category: Optional[str] = None
    created_by_ai: Optional[bool] = False
    created_at: Optional[datetime] = None
    due_date: Optional[date] = None
    rewards_xp: Optional[int] = 0
    rewards_custom_reward: Optional[str] = None
    rewards_unlock: Optional[str] = None
    group_id: Optional[str] = None
    assigned_user_ids: List[str] = []

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    creator_id: Optional[str] = None
    category: Optional[str] = None
    created_by_ai: Optional[bool] = None
    created_at: Optional[datetime] = None
    due_date: Optional[date] = None
    rewards_xp: Optional[int] = None
    rewards_custom_reward: Optional[str] = None
    rewards_unlock: Optional[str] = None
    group_id: Optional[str] = None
    assigned_user_ids: Optional[List[str]] = None

class Goal(GoalBase):
    id: str
    class Config:
        from_attributes = True

class ExplorationStateBase(BaseModel):
    unlocked_locations: List[str] = []
    current_location: Optional[str] = None
    lore_progress: Optional[str] = None
    achievements: List[str] = []

class ExplorationStateCreate(ExplorationStateBase):
    user_id: str

class ExplorationStateUpdate(BaseModel):
    unlocked_locations: Optional[List[str]] = None
    current_location: Optional[str] = None
    lore_progress: Optional[str] = None
    achievements: Optional[List[str]] = None

class ExplorationState(ExplorationStateBase):
    user_id: str
    class Config:
        from_attributes = True

class AchievementBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    xp_reward: Optional[int] = 0

class AchievementCreate(AchievementBase):
    pass

class AchievementUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    xp_reward: Optional[int] = None

class Achievement(AchievementBase):
    id: str
    class Config:
        from_attributes = True

class FocusSessionBase(BaseModel):
    user_id: str
    method: str
    started_at: datetime
    duration: int
    goal_id: Optional[str] = None

class FocusSessionCreate(FocusSessionBase):
    pass

class FocusSessionUpdate(BaseModel):
    user_id: Optional[str] = None
    method: Optional[str] = None
    started_at: Optional[datetime] = None
    duration: Optional[int] = None
    goal_id: Optional[str] = None

class FocusSession(FocusSessionBase):
    id: str
    class Config:
        from_attributes = True

import uuid

from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Table, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base

# Association tables
user_group = Table(
    'user_group', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('group_id', String, ForeignKey('groups.id'))
)
group_goal = Table(
    'group_goal', Base.metadata,
    Column('group_id', String, ForeignKey('groups.id')),
    Column('goal_id', String, ForeignKey('goals.id'))
)
goal_user = Table(
    'goal_user', Base.metadata,
    Column('goal_id', String, ForeignKey('goals.id')),
    Column('user_id', String, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    routine_description = Column(Text)
    available_time = Column(String)
    focus_preference = Column(String)
    group_id = Column(String, ForeignKey('groups.id'), nullable=True)
    current_location = Column(String)
    experience_points = Column(Integer, default=0)
    rank = Column(String)
    streak_days = Column(Integer, default=0)
    hashed_password = Column(String)
    groups = relationship('Group', secondary=user_group, back_populates='members')
    goals = relationship('Goal', secondary=goal_user, back_populates='assigned_users')
    focus_sessions = relationship('FocusSession', back_populates='user')
    exploration_state = relationship('ExplorationState', uselist=False, back_populates='user')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    code = Column(String, unique=True, index=True)
    ship_type = Column(String)
    motto = Column(String)
    progress = Column(Float, default=0.0)
    members = relationship('User', secondary=user_group, back_populates='groups')
    shared_goals = relationship('Goal', secondary=group_goal, back_populates='groups')

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(Text)
    type = Column(String)
    status = Column(String)
    creator_id = Column(String, ForeignKey('users.id'))
    category = Column(String)
    created_by_ai = Column(Boolean, default=False)
    created_at = Column(DateTime)
    due_date = Column(Date)
    rewards_xp = Column(Integer, default=0)
    rewards_custom_reward = Column(String)
    rewards_unlock = Column(String)
    assigned_users = relationship('User', secondary=goal_user, back_populates='goals')
    groups = relationship('Group', secondary=group_goal, back_populates='shared_goals')

class ExplorationState(Base):
    __tablename__ = 'exploration_states'
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    unlocked_locations = Column(Text)  # Store as comma-separated string
    current_location = Column(String)
    lore_progress = Column(String)
    achievements = Column(Text)  # Store as comma-separated string
    user = relationship('User', back_populates='exploration_state')

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True)
    name = Column(String)
    description = Column(Text)
    icon = Column(String)
    xp_reward = Column(Integer, default=0)

class FocusSession(Base):
    __tablename__ = 'focus_sessions'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    method = Column(String)
    started_at = Column(DateTime)
    duration = Column(Integer)
    goal_id = Column(String, ForeignKey('goals.id'), nullable=True)
    user = relationship('User', back_populates='focus_sessions')

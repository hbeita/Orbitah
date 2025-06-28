from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas, utils


# --- USER CRUD ---
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        avatar_url=user.avatar_url,
        routine_description=user.routine_description,
        available_time=user.available_time,
        focus_preference=user.focus_preference,
        group_id=user.group_id,
        current_location=user.current_location,
        experience_points=user.experience_points,
        rank=user.rank,
        streak_days=user.streak_days,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user

# --- GROUP CRUD ---
def get_group(db: Session, group_id: str):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: str, group: schemas.GroupUpdate):
    db_group = get_group(db, group_id)
    for field, value in group.model_dump(exclude_unset=True).items():
        setattr(db_group, field, value)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: str):
    db_group = get_group(db, group_id)
    db.delete(db_group)
    db.commit()
    return db_group

# --- GOAL CRUD ---
def get_goal(db: Session, goal_id: str):
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()

def get_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).offset(skip).limit(limit).all()

def create_goal(db: Session, goal: schemas.GoalCreate):
    db_goal = models.Goal(
        title=goal.title,
        description=goal.description,
        type=goal.type,
        status=goal.status,
        creator_id=goal.creator_id,
        category=goal.category,
        created_by_ai=goal.created_by_ai,
        created_at=goal.created_at or datetime.utcnow(),
        due_date=goal.due_date,
        rewards_xp=goal.rewards_xp,
        rewards_custom_reward=goal.rewards_custom_reward,
        rewards_unlock=goal.rewards_unlock
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: str, goal: schemas.GoalUpdate):
    db_goal = get_goal(db, goal_id)
    for field, value in goal.model_dump(exclude_unset=True).items():
        setattr(db_goal, field, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: str):
    db_goal = get_goal(db, goal_id)
    db.delete(db_goal)
    db.commit()
    return db_goal

# --- EXPLORATION STATE CRUD ---
def get_exploration_state(db: Session, user_id: str):
    state = db.query(models.ExplorationState).filter(models.ExplorationState.user_id == user_id).first()
    if state:
        # Convert comma-separated strings to lists only if needed
        if isinstance(state.unlocked_locations, str):
            state.unlocked_locations = state.unlocked_locations.split(',') if state.unlocked_locations else []
        if isinstance(state.achievements, str):
            state.achievements = state.achievements.split(',') if state.achievements else []
    return state

def create_exploration_state(db: Session, state: schemas.ExplorationStateCreate):
    db_state = models.ExplorationState(
        user_id=state.user_id,
        unlocked_locations=','.join(state.unlocked_locations),
        current_location=state.current_location,
        lore_progress=state.lore_progress,
        achievements=','.join(state.achievements)
    )
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    # Convert for API response
    if isinstance(db_state.unlocked_locations, str):
        db_state.unlocked_locations = db_state.unlocked_locations.split(',') if db_state.unlocked_locations else []
    if isinstance(db_state.achievements, str):
        db_state.achievements = db_state.achievements.split(',') if db_state.achievements else []
    return db_state

def update_exploration_state(db: Session, user_id: str, state: schemas.ExplorationStateUpdate):
    db_state = get_exploration_state(db, user_id)
    for field, value in state.model_dump(exclude_unset=True).items():
        if field in ['unlocked_locations', 'achievements']:
            if value is None:
                continue  # Don't update if not provided
            if isinstance(value, list):
                value = ','.join(value)
        setattr(db_state, field, value)
    # Ensure these fields are always strings before commit
    if isinstance(db_state.unlocked_locations, list):
        db_state.unlocked_locations = ','.join(db_state.unlocked_locations)
    if isinstance(db_state.achievements, list):
        db_state.achievements = ','.join(db_state.achievements)
    db.commit()
    db.refresh(db_state)
    # Convert for API response
    if isinstance(db_state.unlocked_locations, str):
        db_state.unlocked_locations = db_state.unlocked_locations.split(',') if db_state.unlocked_locations else []
    if isinstance(db_state.achievements, str):
        db_state.achievements = db_state.achievements.split(',') if db_state.achievements else []
    return db_state

def delete_exploration_state(db: Session, user_id: str):
    db_state = get_exploration_state(db, user_id)
    db.delete(db_state)
    db.commit()
    return db_state

# --- ACHIEVEMENT CRUD ---
def get_achievement(db: Session, achievement_id: str):
    return db.query(models.Achievement).filter(models.Achievement.id == achievement_id).first()

def get_achievements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Achievement).offset(skip).limit(limit).all()

def create_achievement(db: Session, achievement: schemas.AchievementCreate):
    db_achievement = models.Achievement(**achievement.model_dump())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement

def update_achievement(db: Session, achievement_id: str, achievement: schemas.AchievementUpdate):
    db_achievement = get_achievement(db, achievement_id)
    for field, value in achievement.model_dump(exclude_unset=True).items():
        setattr(db_achievement, field, value)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement

def delete_achievement(db: Session, achievement_id: str):
    db_achievement = get_achievement(db, achievement_id)
    db.delete(db_achievement)
    db.commit()
    return db_achievement

# --- FOCUS SESSION CRUD ---
def get_focus_session(db: Session, session_id: str):
    return db.query(models.FocusSession).filter(models.FocusSession.id == session_id).first()

def get_focus_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FocusSession).offset(skip).limit(limit).all()

def create_focus_session(db: Session, session: schemas.FocusSessionCreate):
    db_session = models.FocusSession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_focus_session(db: Session, session_id: str, session: schemas.FocusSessionUpdate):
    db_session = get_focus_session(db, session_id)
    for field, value in session.model_dump(exclude_unset=True).items():
        setattr(db_session, field, value)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete_focus_session(db: Session, session_id: str):
    db_session = get_focus_session(db, session_id)
    db.delete(db_session)
    db.commit()
    return db_session

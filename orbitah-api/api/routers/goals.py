from typing import List

from api import crud, schemas
from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("/", response_model=schemas.Goal)
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    return crud.create_goal(db, goal)

@router.get("/", response_model=List[schemas.Goal])
def read_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goals(db, skip=skip, limit=limit)

@router.get("/{goal_id}", response_model=schemas.Goal)
def read_goal(goal_id: str, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

@router.put("/{goal_id}", response_model=schemas.Goal)
def update_goal(goal_id: str, goal: schemas.GoalUpdate, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.update_goal(db, goal_id, goal)

@router.delete("/{goal_id}", response_model=schemas.Goal)
def delete_goal(goal_id: str, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.delete_goal(db, goal_id)

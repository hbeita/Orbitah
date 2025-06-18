from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/exploration", tags=["exploration"])

@router.post("/", response_model=schemas.ExplorationState)
def create_exploration_state(state: schemas.ExplorationStateCreate, db: Session = Depends(get_db)):
    return crud.create_exploration_state(db, state)

@router.get("/{user_id}", response_model=schemas.ExplorationState)
def read_exploration_state(user_id: str, db: Session = Depends(get_db)):
    db_state = crud.get_exploration_state(db, user_id=user_id)
    if db_state is None:
        raise HTTPException(status_code=404, detail="Exploration state not found")
    return db_state

@router.put("/{user_id}", response_model=schemas.ExplorationState)
def update_exploration_state(user_id: str, state: schemas.ExplorationStateUpdate, db: Session = Depends(get_db)):
    db_state = crud.get_exploration_state(db, user_id=user_id)
    if db_state is None:
        raise HTTPException(status_code=404, detail="Exploration state not found")
    return crud.update_exploration_state(db, user_id, state)

@router.delete("/{user_id}", response_model=schemas.ExplorationState)
def delete_exploration_state(user_id: str, db: Session = Depends(get_db)):
    db_state = crud.get_exploration_state(db, user_id=user_id)
    if db_state is None:
        raise HTTPException(status_code=404, detail="Exploration state not found")
    return crud.delete_exploration_state(db, user_id)

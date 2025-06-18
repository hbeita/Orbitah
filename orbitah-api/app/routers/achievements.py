from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/achievements", tags=["achievements"])

@router.post("/", response_model=schemas.Achievement)
def create_achievement(achievement: schemas.AchievementCreate, db: Session = Depends(get_db)):
    return crud.create_achievement(db, achievement)

@router.get("/", response_model=List[schemas.Achievement])
def read_achievements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_achievements(db, skip=skip, limit=limit)

@router.get("/{achievement_id}", response_model=schemas.Achievement)
def read_achievement(achievement_id: str, db: Session = Depends(get_db)):
    db_achievement = crud.get_achievement(db, achievement_id=achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return db_achievement

@router.put("/{achievement_id}", response_model=schemas.Achievement)
def update_achievement(achievement_id: str, achievement: schemas.AchievementUpdate, db: Session = Depends(get_db)):
    db_achievement = crud.get_achievement(db, achievement_id=achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return crud.update_achievement(db, achievement_id, achievement)

@router.delete("/{achievement_id}", response_model=schemas.Achievement)
def delete_achievement(achievement_id: str, db: Session = Depends(get_db)):
    db_achievement = crud.get_achievement(db, achievement_id=achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return crud.delete_achievement(db, achievement_id)

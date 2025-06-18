from typing import List

from api import crud, schemas
from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/focus_sessions", tags=["focus_sessions"])

@router.post("/", response_model=schemas.FocusSession)
def create_focus_session(session: schemas.FocusSessionCreate, db: Session = Depends(get_db)):
    return crud.create_focus_session(db, session)

@router.get("/", response_model=List[schemas.FocusSession])
def read_focus_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_focus_sessions(db, skip=skip, limit=limit)

@router.get("/{session_id}", response_model=schemas.FocusSession)
def read_focus_session(session_id: str, db: Session = Depends(get_db)):
    db_session = crud.get_focus_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Focus session not found")
    return db_session

@router.put("/{session_id}", response_model=schemas.FocusSession)
def update_focus_session(session_id: str, session: schemas.FocusSessionUpdate, db: Session = Depends(get_db)):
    db_session = crud.get_focus_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Focus session not found")
    return crud.update_focus_session(db, session_id, session)

@router.delete("/{session_id}", response_model=schemas.FocusSession)
def delete_focus_session(session_id: str, db: Session = Depends(get_db)):
    db_session = crud.get_focus_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Focus session not found")
    return crud.delete_focus_session(db, session_id)

from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Task, User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def create_task(title: str,
                description: str = "",
                phase: str = "",
                urgency: str = "",
                location: str = "",
                responsible_id: Optional[int] = None,
                due_date: Optional[date] = None,
                db: Session = Depends(get_db)):
    task = Task(
        title=title,
        description=description,
        phase=phase,
        urgency=urgency,
        location=location,
        responsible_id=responsible_id,
        due_date=due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"msg": "task created", "id": task.id}


@router.get("/")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "phase": t.phase,
            "urgency": t.urgency,
            "location": t.location,
            "responsible_id": t.responsible_id,
            "due_date": t.due_date,
        }
        for t in tasks
    ]


@router.put("/{task_id}")
def update_task(task_id: int,
                title: Optional[str] = None,
                description: Optional[str] = None,
                phase: Optional[str] = None,
                urgency: Optional[str] = None,
                location: Optional[str] = None,
                status: Optional[str] = None,
                responsible_id: Optional[int] = None,
                due_date: Optional[date] = None,
                db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if phase is not None:
        task.phase = phase
    if urgency is not None:
        task.urgency = urgency
    if location is not None:
        task.location = location
    if status is not None:
        task.status = status
    if responsible_id is not None:
        task.responsible_id = responsible_id
    if due_date is not None:
        task.due_date = due_date
    db.commit()
    db.refresh(task)
    return {"msg": "task updated"}


@router.get("/reports/{period}")
def task_report(period: str, db: Session = Depends(get_db)):
    if period not in {"daily", "weekly"}:
        raise HTTPException(status_code=400, detail="Invalid period")
    now = datetime.utcnow().date()
    if period == "daily":
        start = now
    else:  # weekly
        start = now - timedelta(days=7)
    tasks = db.query(Task).filter(Task.updated_at >= start).all()
    summary = {
        "total": len(tasks),
        "by_status": {},
    }
    for t in tasks:
        summary["by_status"].setdefault(t.status, 0)
        summary["by_status"][t.status] += 1
    return summary

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .database import Base, engine
from .routers import auth, dashboard, files, tasks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ORE Web App")

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(files.router)
app.include_router(tasks.router)

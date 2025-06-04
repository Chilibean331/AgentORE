from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import json
import sqlite3
from collections import Counter
from datetime import datetime

from ..database import get_db
from ..models import User, StoredFile

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):
    users = db.query(User).count()
    files = db.query(StoredFile).count()
    return {"users": users, "files": files}


@router.get("/mission-data")
def mission_data():
    root = Path(__file__).resolve().parents[4]
    contacts_file = root / "contacts_data" / "contacts.json"
    osint_db = root / "ORE" / "osint" / "ore_osint.db"

    data = {
        "map": [],
        "time_series": [],
        "active_contacts": 0,
        "last_report": None,
        "open_incidents": 0,
    }

    if contacts_file.exists():
        try:
            with open(contacts_file, "r", encoding="utf-8") as f:
                contacts = json.load(f).get("contacts", [])
                data["active_contacts"] = len(contacts)
        except Exception:
            pass

    if osint_db.exists():
        try:
            conn = sqlite3.connect(osint_db)
            cur = conn.execute(
                "SELECT timestamp, latitude, longitude, title FROM intel"
            )
            rows = cur.fetchall()
            data["open_incidents"] = len(rows)
            last = None
            counter = Counter()
            for ts, lat, lon, title in rows:
                if lat is not None and lon is not None:
                    data["map"].append({"lat": lat, "lon": lon, "title": title})
                if ts:
                    try:
                        dt = datetime.fromisoformat(ts)
                    except ValueError:
                        try:
                            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                        except Exception:
                            continue
                    counter[dt.date().isoformat()] += 1
                    if not last or dt > last:
                        last = dt
            data["time_series"] = sorted(counter.items())
            data["last_report"] = last.isoformat() if last else None
        finally:
            conn.close()

    return data

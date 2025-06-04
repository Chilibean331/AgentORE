from datetime import datetime
import uuid
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from fpdf import FPDF

from ..database import get_db
from ..models import Report, ReportFile, StoredFile
from ..encryption import encrypt_data

router = APIRouter(prefix="/reports", tags=["reports"])


def generate_reference() -> str:
    return "REP-" + datetime.utcnow().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:6]


@router.post("/")
async def create_report(
    details: str,
    latitude: float,
    longitude: float,
    tags: str,
    priority: str,
    follow_up: bool = False,
    files: list[UploadFile] | None = File(None),
    db: Session = Depends(get_db),
):
    reference = generate_reference()
    report = Report(
        reference=reference,
        details=details,
        latitude=latitude,
        longitude=longitude,
        tags=tags,
        priority=priority,
        follow_up=follow_up,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    if files:
        for upload in files:
            raw = await upload.read()
            encrypted = encrypt_data(raw)
            stored = StoredFile(filename=upload.filename, data=encrypted)
            db.add(stored)
            db.commit()
            db.refresh(stored)
            link = ReportFile(report_id=report.id, file_id=stored.id)
            db.add(link)
            db.commit()

    return {"id": report.id, "reference": report.reference}


@router.get("/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "id": report.id,
        "reference": report.reference,
        "details": report.details,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "tags": report.tags,
        "priority": report.priority,
        "follow_up": report.follow_up,
        "status": report.status,
        "attachments": [f.file_id for f in report.files],
    }


@router.get("/{report_id}/pdf")
def export_report_pdf(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Report {report.reference}", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Details: {report.details}")
    pdf.cell(0, 10, f"Location: {report.latitude}, {report.longitude}", ln=1)
    pdf.cell(0, 10, f"Tags: {report.tags}", ln=1)
    pdf.cell(0, 10, f"Priority: {report.priority}", ln=1)
    pdf.cell(0, 10, f"Follow Up: {report.follow_up}", ln=1)
    pdf.cell(0, 10, f"Status: {report.status}", ln=1)
    data = pdf.output(dest="S").encode("latin-1")
    return Response(content=data, media_type="application/pdf")

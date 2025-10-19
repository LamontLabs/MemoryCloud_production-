import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.memorycloud.store import list_memories
from src.memorycloud.config import settings

EXPORT_DIR = "dist/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_json():
    data = list_memories()
    path = os.path.join(EXPORT_DIR, f"memories_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

def export_pdf():
    path = os.path.join(EXPORT_DIR, f"memories_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf")
    c = canvas.Canvas(path, pagesize=letter)
    text_object = c.beginText(40, 750)
    text_object.setFont("Helvetica", 10)
    text_object.textLine("MemoryCloud — Demo Export")
    text_object.textLine(f"Date: {datetime.utcnow().isoformat()}")
    text_object.textLine("")
    for entry in list_memories():
        text_object.textLine(f"[{entry['created_at']}] {entry['text']} (indicator={entry['indicator']})")
    c.drawText(text_object)
    c.showPage()
    c.save()
    return path

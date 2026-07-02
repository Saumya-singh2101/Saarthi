import logging
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pipeline_engine import run_pipeline
from models import ContinuityRequest, AnalyzeResponse

from database import (
    get_patient_by_card,
    get_history,
    get_current_medications,
)

from translator import translate_text
from translator import translate_record
from pydantic import BaseModel

from synthetic_surveillance import generate_cases
from surveillance_engine import detect_anomalies, build_trend

app = FastAPI(title="Saarthi — Continuity of Care API")

# Updated CORS configuration to allow Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://saarthi-ecru-six.vercel.app",  # Allowed your deployed Vercel frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    
class RecordTranslateRequest(BaseModel):
    payload: dict
    target_language: str

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: ContinuityRequest):
    result = run_pipeline(
        request.health_card_id,
        request.symptoms,
    )

    return {
        "status": "success",
        "data": result,
    }


@app.get("/patient/{card_id}")
def get_patient_record(card_id: str):

    patient = get_patient_by_card(card_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient_uuid = patient["patient_id"]

    history = get_history(patient_uuid)
    # Corrected indentation for medications to prevent potential scope issues
    medications = get_current_medications(patient_uuid)

    return {
        "status": "success",
        "patient": {
            "health_card_id": card_id,
            "full_name": patient.get("full_name"),
            "age": patient.get("age"),
            "gender": patient.get("gender"),
            "blood_group": patient.get("blood_group"),
            "phone": patient.get("phone"),
            "allergies": patient.get("allergies"),
        },
        "medical_history": history,
        "current_medications": medications,
    }
    
@app.post("/translate")
def translate(req: TranslateRequest):
    return {"status": "success", "translated": translate_text(req.text, req.target_language)}

@app.post("/translate-record")
def translate_record_endpoint(req: RecordTranslateRequest):
    return {"status": "success", "translated": translate_record(req.payload, req.target_language)}

@app.get("/surveillance")
def surveillance():
    records = generate_cases()
    alerts = detect_anomalies(records)

    # attach a trend line to each alert for charting
    for a in alerts:
        a["trend"] = build_trend(records, a["settlement"], a["symptom"])

    # settlement totals for an overview panel
    totals = {}
    for r in records:
        totals[r["settlement"]] = totals.get(r["settlement"], 0) + r["count"]

    return {
        "status": "success",
        "synthetic": True,   # honesty flag, surfaced in the UI
        "alerts": alerts,
        "settlement_totals": totals,
        "monitored_settlements": len(set(r["settlement"] for r in records)),
        "monitored_symptoms": len(set(r["symptom"] for r in records)),
    }

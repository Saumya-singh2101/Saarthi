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
from pydantic import BaseModel

app = FastAPI(title="Saarthi — Continuity of Care API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslateRequest(BaseModel):
    text: str
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
        },
        "medical_history": history,
        "current_medications": medications,
    }
    
@app.post("/translate")
def translate(req: TranslateRequest):
    return {"status": "success", "translated": translate_text(req.text, req.target_language)}
from fastapi import APIRouter, HTTPException

from models import ContinuityRequest

from database import (
    get_patient,
    get_history,
    get_current_medications
)

from context_engine import extract_relevant_history
from risk_engine import generate_risk_flags
from prompt_builder import build_prompt
from groq_client import generate_continuity_report

from rag import (
    index_patient_history,
    retrieve_history
)

router = APIRouter(
    prefix="/api/v1/continuity",
    tags=["AI Continuity Engine"]
)


@router.post("/report")
def continuity_report(request: ContinuityRequest):

    # ---------------------------------
    # Step 1 : Fetch Patient
    # ---------------------------------

    patient = get_patient(request.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # ---------------------------------
    # Step 2 : Fetch Medical History
    # ---------------------------------

    history = get_history(request.patient_id)

    # ---------------------------------
    # Step 3 : Fetch Current Medicines
    # ---------------------------------

    medications = get_current_medications(request.patient_id)

    # ---------------------------------
    # Step 4 : Index Records into RAG
    # ---------------------------------

    if history:
        index_patient_history(
            request.patient_id,
            history
        )

    # ---------------------------------
    # Step 5 : Retrieve Relevant History
    # ---------------------------------

    relevant_history = retrieve_history(
        request.symptoms
    )

    # ---------------------------------
    # Step 6 : Risk Engine
    # ---------------------------------

    risks = generate_risk_flags(
        patient,
        history
    )

    # ---------------------------------
    # Step 7 : Prompt Builder
    # ---------------------------------

    prompt = build_prompt(
        patient=patient,
        symptoms=request.symptoms,
        history=relevant_history,
        medicines=medications,
        risks=risks
    )

    # ---------------------------------
    # Step 8 : Generate AI Report
    # ---------------------------------

    ai_report = generate_continuity_report(
        prompt
    )

    # ---------------------------------
    # Step 9 : Return Response
    # ---------------------------------

    return {
        "patient": patient["full_name"],
        "summary": ai_report.get("summary", ""),
        "relevant_history": ai_report.get("relevant_history", []),
        "current_medications": [
            medicine["medicine_name"]
            for medicine in medications
        ],
        "red_flags": ai_report.get("red_flags", []),
        "suggested_tests": ai_report.get("suggested_tests", []),
        "drug_interactions": ai_report.get("drug_interactions", [])
    }
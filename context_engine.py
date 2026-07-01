def extract_relevant_history(history, symptoms):

    symptoms = symptoms.lower()

    relevant = []

    keywords = {
        "chest": ["Diabetes", "Hypertension", "Heart Disease"],
        "cough": ["Asthma", "Tuberculosis"],
        "fever": ["Typhoid", "Malaria", "Dengue"],
        "breathing": ["Asthma"]
    }

    diseases = []

    for word in keywords:

        if word in symptoms:
            diseases.extend(keywords[word])

    for record in history:

        if record["disease_name"] in diseases:
            relevant.append(record)

    if len(relevant) == 0:
        relevant = history

    return relevant

# context_engine.py
# context_engine.py

from database import get_patient_by_card, get_history, get_current_medications

def build_context(health_card_id):
    patient = get_patient_by_card(health_card_id) or {}
    patient_uuid = patient.get("patient_id")

    raw_history = get_history(patient_uuid) if patient_uuid else []
    raw_meds = get_current_medications(patient_uuid) if patient_uuid else []

    history = [
        {
            "disease_name": h.get("disease_name", ""),
            "diagnosis_date": h.get("diagnosis_date", ""),
        }
        for h in raw_history
    ]
    medications = [{"name": m.get("medicine_name", "")} for m in raw_meds]
    
    raw_allergies = patient.get("allergies") or ""

    allergies = [
        allergy.strip()
        for allergy in raw_allergies.split(",")
        if allergy.strip()
    ]

    return {
        "patient_id": patient_uuid,
        "patient": {
            "full_name": patient.get("full_name", "Unknown"),
            "age": patient.get("age", "Unknown"),
            "allergies": allergies,
        },
        "history": history,
        "medications": medications,
    }
# rag.py (HACKATHON SAFE VERSION - NO CHROMADB)

def retrieve_context(query):
    return {
        "documents": [
            "Patient has hypertension history",
            "No critical drug interaction detected in basic dataset",
            "Previous medication: beta blockers (mock data)"
        ]
    }


def index_patient_history(patient_id, history):
    # Mock function (not used in Feature 1)
    return True


def retrieve_history(symptoms):
    # Mock function (not used in Feature 1)
    return [
        "Sample medical record 1",
        "Sample medical record 2"
    ]
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
def build_context(patient_id):
    """Mock context for Feature 1. Same shape the Supabase query will return later."""
    return {
        "patient_id": patient_id,
        "patient": {"full_name": "Ramesh Kumar", "age": 42},
        "medications": [{"name": "Warfarin"}, {"name": "Ibuprofen"}],
        "history": [
            {"disease_name": "Hypertension"},
            {"disease_name": "Type 2 Diabetes"},
        ],
    }
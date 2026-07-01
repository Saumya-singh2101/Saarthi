def build_prompt(context, risk_data, rag_data, query):

    patient = context.get("patient", {})
    allergies = patient.get("allergies", [])
    allergy_text = ", ".join(allergies) if allergies else "None reported"
    history = context.get("history", [])
    medicines = context.get("medications", [])

    sorted_history = sorted(
        history, key=lambda h: h.get("diagnosis_date", "")
    ) if history else []
    disease_history = "\n".join(
        f"{h.get('diagnosis_date', 'date unknown')}: {h.get('disease_name', '')}"
        for h in sorted_history
    ) if sorted_history else "None"

    medication_list = "\n".join(
        [m.get("name", "") for m in medicines]
    ) if medicines else "None"

    risk_text = "\n".join(
        risk_data.get("explanations", [])
    ) if risk_data else "None"

    prompt = f"""
You are an AI clinical assistant.

Patient Name:
{patient.get("full_name", "Unknown")}

Age:
{patient.get("age", "Unknown")}

User Query:
{query}

Relevant Medical History:
{disease_history}

Current Medications:
{medication_list}

Known Allergies:
{allergy_text}

Risk Flags:
{risk_text}

RAG Context:
{rag_data}

Return JSON ONLY with:
summary,
relevant_history,
allergy_alerts,
red_flags,
suggested_tests,
drug_interactions

If any current medication, suggested test, or treatment could conflict with the patient's known allergies, include a clear explanation in allergy_alerts.

Do NOT diagnose.
"""

    return prompt
def build_prompt(context, risk_data, rag_data, query):

    patient = context.get("patient", {})
    history = context.get("history", [])
    medicines = context.get("medications", [])

    disease_history = "\n".join(
        h.get("disease_name", "") for h in history
    ) if history else "None"

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

Risk Flags:
{risk_text}

RAG Context:
{rag_data}

Return JSON ONLY with:
summary,
relevant_history,
red_flags,
suggested_tests,
drug_interactions

Do NOT diagnose.
"""

    return prompt
# response_parser.py

import json

def parse_response(raw_response, risk_data):
    """
    Converts Groq raw output → structured API response
    """

    try:
        llm_output = json.loads(raw_response)
    except:
        llm_output = {
            "summary": raw_response,
            "recommendations": []
        }

    structured_response = {
        "summary": llm_output.get("summary", ""),
        "recommendations": llm_output.get("recommendations", []),
        "risk_score": risk_data.get("risk_score", 0),
        "risk_flags": risk_data.get("flags", []),
        "medication_alerts": llm_output.get("medication_alerts", []),
        "follow_up": llm_output.get("follow_up", None)
    }

    return structured_response
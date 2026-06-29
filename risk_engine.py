# risk_engine.py

def analyze_risk(context):
    meds = context.get("medications", [])

    score = 0
    flags = []
    explanations = []

    for m in meds:
        name = m.get("name", "").lower()

        if "warfarin" in name:
            score += 40
            flags.append("BLOOD_THINNER")
            explanations.append("Warfarin increases bleeding risk")

        if "ibuprofen" in name:
            score += 20
            flags.append("NSAID")
            explanations.append("May affect stomach/kidneys")

        if "insulin" in name:
            score += 25
            flags.append("DIABETES_MED")
            explanations.append("Needs sugar monitoring")

    level = "LOW"
    if score > 60:
        level = "HIGH"
    elif score > 30:
        level = "MEDIUM"

    return {
        "risk_score": score,
        "risk_level": level,
        "flags": flags,
        "explanations": explanations
    }
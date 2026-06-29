INTERACTIONS = {
    ("warfarin", "ibuprofen"): "High bleeding risk",
    ("aspirin", "clopidogrel"): "Bleeding risk increase",
    ("insulin", "prednisone"): "Blood sugar spike risk"
}

def check_interactions(meds):
    meds = [m.get("name", "").lower() for m in meds]

    alerts = []

    for i in range(len(meds)):
        for j in range(i + 1, len(meds)):

            pair = (meds[i], meds[j])
            reverse = (meds[j], meds[i])

            if pair in INTERACTIONS:
                alerts.append({
                    "pair": pair,
                    "risk": INTERACTIONS[pair]
                })

            if reverse in INTERACTIONS:
                alerts.append({
                    "pair": reverse,
                    "risk": INTERACTIONS[reverse]
                })

    return alerts
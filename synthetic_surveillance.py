import random
from datetime import date, timedelta

# Fixed seed → same outbreak every run, so your demo is reproducible
random.seed(42)

SETTLEMENTS = ["Dharavi", "Govandi", "Mankhurd", "Kurla", "Bhandup"]
SYMPTOMS = ["Fever", "Cough", "Diarrhea", "Body Ache", "Rash"]

def generate_cases(days=14):
    """Synthetic daily case counts per settlement+symptom.
    A fever outbreak is planted in Govandi over the final 3 days."""
    today = date.today()
    records = []

    for d in range(days):
        day = today - timedelta(days=(days - 1 - d))
        for settlement in SETTLEMENTS:
            for symptom in SYMPTOMS:
                count = random.randint(0, 4)  # baseline noise

                # planted outbreak: Govandi fever ramps up sharply at the end
                if settlement == "Govandi" and symptom == "Fever" and d >= days - 3:
                    count += (d - (days - 4)) * 12

                records.append({
                    "date": day.isoformat(),
                    "settlement": settlement,
                    "symptom": symptom,
                    "count": count,
                })
    return records
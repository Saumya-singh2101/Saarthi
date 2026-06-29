from fastapi import FastAPI
from pipeline_engine import run_pipeline

app = FastAPI()

@app.post("/analyze")
def analyze(data: dict):
    patient_id = data.get("patient_id")
    query = data.get("query")

    result = run_pipeline(patient_id, query)

    return {
        "status": "success",
        "data": result
    }
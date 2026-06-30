from pydantic import BaseModel

class ContinuityRequest(BaseModel):
    health_card_id: str
    symptoms: str

class ContinuityResponse(BaseModel):
    summary: str
    relevant_history: list = []
    current_medications: list = []
    red_flags: list = []
    suggested_tests: list = []
    drug_interactions: list = []
    risk_score: int = 0
    risk_level: str = "LOW"
    risk_flags: list = []

class AnalyzeResponse(BaseModel):
    status: str
    data: ContinuityResponse
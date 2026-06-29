from pydantic import BaseModel


class ContinuityRequest(BaseModel):

    patient_id:str

    symptoms:str


class ContinuityResponse(BaseModel):

    summary:str

    relevant_history:list

    current_medications:list

    red_flags:list

    suggested_tests:list

    drug_interactions:list
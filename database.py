import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------
# Get Patient Details
# -----------------------------
def get_patient(patient_id: str):

    response = (
        supabase.table("patients")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# -----------------------------
# Get Medical History
# -----------------------------
def get_history(patient_id: str):

    response = (
        supabase.table("medical_history")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    return response.data if response.data else []


# -----------------------------
# Get Current Medications
# -----------------------------
def get_current_medications(patient_id: str):

    response = (
        supabase.table("medications")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    return response.data if response.data else []

def get_patient_by_card(card_id: str):
    response = (
        supabase.table("patients")
        .select("*")
        .eq("health_card_id", card_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    return None
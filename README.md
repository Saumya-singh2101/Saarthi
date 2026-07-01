# Saarthi — Your Health Companion

**Portable, QR-linked digital health records for India's migrant workforce.**

Saarthi gives every migrant worker a health record that lives on a QR card, not a phone. A doctor in any city scans the card and instantly sees the worker's full history — no app or internet needed on the worker's side — plus an AI-generated continuity-of-care report linking past history to current symptoms.

Built by **Team ExploreeTinkerBell** for **Evolothon 1.0** (Health & EdTech).

---

## The Problem

When a migrant worker moves between states, their medical history doesn't move with them. Every new hospital starts from zero — repeat tests, delays, and broken continuity of care. Prescriptions in an unfamiliar language cause medication errors, and outbreaks in dense settlements go unnoticed until late.

## What Saarthi Does

- **AI Continuity-of-Care Report** — scan a card, enter symptoms, get a structured clinical briefing (history, red flags, suggested tests, drug interactions, allergy alerts, risk level).
- **Multilingual Records** — the report renders in 8 languages; drug names are never translated, for safety.
- **Health Timeline** — a chronological visual of the patient's medical journey, also fed to the AI as context.
- **AI Outbreak Surveillance** — statistical spike detection flags disease clusters early (demonstrated on synthetic data).
- **Two-role access** — hospital-verified records; doctors read/write, patients view-only.

---

## Tech Stack

| Layer | Stack |
|---|---|
| Frontend | React 18, Vite, Recharts, html5-qrcode |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| Database & Auth | Supabase (PostgreSQL, Row-Level Security, Auth) |
| AI | Groq — `llama-3.3-70b-versatile` |
| ML | Z-score anomaly detection |

---

## Architecture

The system has three layers: a **React client** (login, doctor console, patient view, surveillance dashboard), a **stateless FastAPI layer** exposing the core endpoints, and a **data/AI layer** (Supabase for records + auth, Groq for inference). A continuity request flows through a single pipeline: read & normalize the record → deterministic risk/interaction checks → timeline-aware prompt → LLM inference → structured, validated response. Safety-critical facts (drug interactions) are computed in code, not by the model.

---

## Project Structure

Saarthi/
├── main.py                    # FastAPI app + endpoints
├── pipeline_engine.py         # Orchestrates the continuity pipeline
├── context_engine.py          # Reads & normalizes records from Supabase
├── prompt_builder.py          # Builds the timeline-aware, allergy-aware prompt
├── groq_client.py             # Groq LLM calls (JSON mode)
├── risk_engine.py             # Deterministic risk scoring
├── interaction_engine.py      # Deterministic drug-interaction checks
├── surveillance_engine.py     # Z-score outbreak detection
├── synthetic_surveillance.py  # Synthetic case-count generator
├── translator.py              # Multilingual translation
├── database.py                # Supabase client + queries
├── models.py                  # Pydantic request/response models
├── requirements.txt
└── frontend/                  # React + Vite app
└── src/
├── App.jsx            # Main app, role routing, doctor console
├── Login.jsx          # Supabase auth
├── Surveillance.jsx   # Outbreak dashboard
├── QrScanner.jsx      # QR card scanning
├── api.js             # Backend API calls
└── supabase.js        # Supabase client (auth)

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Supabase project and a Groq API key

### 1. Backend

```bash
# from the repo root
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Create a `.env` file in the repo root:

GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key

Run the API:

```bash
uvicorn main:app --reload
```

The API serves at `http://127.0.0.1:8000`, with interactive docs at `/docs`.

### 2. Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:

VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

Run the dev server:

```bash
npm run dev
```

The app serves at `http://localhost:5173`.

> **Note on keys:** the backend uses the Supabase **service_role** key (trusted server code); the frontend uses the **anon** key (browser, for auth only). Both `.env` files are gitignored — never commit real keys.

---

## Database Schema

Supabase (PostgreSQL) with Row-Level Security enabled:

- **patients** — `patient_id`, `health_card_id`, `full_name`, `age`, `gender`, `blood_group`, `allergies`
- **medical_history** — `patient_id`, `disease_name`, `diagnosis_date`, `hospital_name`
- **medications** — `patient_id`, `medicine_name`, `dosage`, `frequency`, `status`
- **profiles** — maps each auth user to a `role` (doctor / patient) and their record

---

## Key Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/analyze` | Generate the AI continuity-of-care report |
| `GET` | `/patient/{card_id}` | Fetch a full patient record |
| `POST` | `/translate` | Translate the report summary |
| `POST` | `/translate-record` | Translate the full report (batch) |
| `GET` | `/surveillance` | Outbreak detection over case data |

---

## Team

- **Nidhi Dhyani** — Frontend + AI/ML
- **Saumya Singh** — Backend + Systems

---

*Saarthi — health records that travel with the worker.*
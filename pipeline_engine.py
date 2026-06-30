from context_engine import build_context
from risk_engine import analyze_risk
from interaction_engine import check_interactions
from rag import retrieve_context
from prompt_builder import build_prompt
from groq_client import get_llm_response


def run_pipeline(health_card_id, query):
    # 1. Get patient data
    context = build_context(health_card_id)

    # 2. Risk analysis
    risk_data = analyze_risk(context)

    # 3. Drug interaction check
    interactions = check_interactions(context.get("medications", []))

    # 4. RAG retrieval
    rag_data = retrieve_context(query)

    # 5. Build prompt
    prompt = build_prompt(context, risk_data, rag_data, query)

    # 6. LLM call
    raw_response = get_llm_response(prompt)

    # 7. Assemble final report (LLM already returns a parsed dict)
    result = {
        "summary":           raw_response.get("summary", ""),
        "relevant_history":  raw_response.get("relevant_history", []),
        "current_medications": [m.get("name", "") for m in context.get("medications", [])],
        "red_flags":         raw_response.get("red_flags", []),
        "suggested_tests":   raw_response.get("suggested_tests", []),
        "drug_interactions": interactions,          # deterministic, NOT LLM-guessed
        "risk_score":        risk_data.get("risk_score", 0),
        "risk_level":        risk_data.get("risk_level", "LOW"),
        "risk_flags":        risk_data.get("flags", []),
    }
    return result
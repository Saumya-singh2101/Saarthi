from context_engine import build_context
from risk_engine import analyze_risk
from interaction_engine import check_interactions
from rag import retrieve_context
from prompt_builder import build_prompt
from groq_client import get_llm_response
from response_parser import parse_response


def run_pipeline(patient_id, query):

    # 1. Get patient data
    context = build_context(patient_id)

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

    # 7. Final parsing
    result = parse_response(raw_response, risk_data)

    # 8. Add interactions
    result["drug_interactions"] = interactions

    return result
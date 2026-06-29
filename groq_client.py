import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("MODEL_NAME")


def generate_continuity_report(prompt):

    try:

        completion = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced clinical decision support assistant. Always return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            max_tokens=2048,
            response_format={"type": "json_object"},
        )

        result = completion.choices[0].message.content

        return json.loads(result)

    except Exception as e:

        print(e)

        return {
            "summary": "Unable to generate report.",
            "relevant_history": [],
            "red_flags": [],
            "suggested_tests": [],
            "drug_interactions": []
        }
    # WRAPPER for pipeline compatibility
def get_llm_response(prompt):
    return generate_continuity_report(prompt)

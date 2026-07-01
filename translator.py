from groq_client import client, MODEL
import json

def translate_text(text, target_language):
    if not text or not text.strip():
        return ""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content":
                f"You are a medical translator. Translate the user's text into {target_language}. "
                "Preserve medicine names and dosages exactly. Return ONLY the translation, no notes."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
        max_tokens=1500,
    )
    return completion.choices[0].message.content.strip()


def translate_record(payload, target_language):
    """Translate a dict of medical fields in ONE call. Returns same keys, translated values.
    Medicine names are preserved (not translated) for safety."""
    if target_language.lower() == "english":
        return payload

    prompt = (
        f"Translate the VALUES in this medical JSON into {target_language}. "
        "Rules: keep medicine/drug names in their original English form (do not translate them). "
        "Translate disease names, instructions, and descriptive text. "
        "Return ONLY valid JSON with the exact same keys and structure, no extra text.\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise medical translator. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2000,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return payload  # fall back to original if parsing fails
from groq_client import client, MODEL

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
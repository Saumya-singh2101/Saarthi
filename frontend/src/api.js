const API_BASE = "http://127.0.0.1:8000";

export async function getPatientRecord(cardId) {
  const res = await fetch(`${API_BASE}/patient/${encodeURIComponent(cardId)}`);
  if (!res.ok) {
    if (res.status === 404) throw new Error("No patient found for this card ID.");
    throw new Error("Couldn't load the record. Is the backend running?");
  }
  return res.json();
}

export async function generateReport(cardId, symptoms) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ health_card_id: cardId, symptoms }),
  });
  if (!res.ok) throw new Error("Report generation failed. Check the backend logs.");
  return res.json();
}

export async function translateText(text, targetLanguage) {
  const res = await fetch(`${API_BASE}/translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, target_language: targetLanguage }),
  });
  if (!res.ok) throw new Error("Translation failed.");
  return (await res.json()).translated;
}
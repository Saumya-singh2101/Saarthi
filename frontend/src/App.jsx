import { useState, useEffect } from "react";
import { getPatientRecord, generateReport, translateText, translateRecord, } from "./api";
import QrScanner from "./QrScanner";
import { supabase } from "./supabase";
import Login from "./Login";
import Surveillance from "./Surveillance";

export default function App() {
  const [cardId, setCardId] = useState("");
  const [record, setRecord] = useState(null);
  const [symptoms, setSymptoms] = useState("");
  const [report, setReport] = useState(null);
  const [loadingRecord, setLoadingRecord] = useState(false);
  const [loadingReport, setLoadingReport] = useState(false);
  const [showScanner, setShowScanner] = useState(false);
  const [error, setError] = useState("");
  const [session, setSession] = useState(null);
  const [profile, setProfile] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [translatedSummary, setTranslatedSummary] = useState("");
  const [translating, setTranslating] = useState(false);
  const [activeLang, setActiveLang] = useState("English");
  const [view, setView] = useState("console"); // "console" | "surveillance"
  const [translatedReport, setTranslatedReport] = useState(null);

  useEffect(() => {
  supabase.auth.getSession().then(({ data }) => {
    setSession(data.session);
    setAuthLoading(false);
  });
  const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s));
  return () => sub.subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (!session) { setProfile(null); return; }
    supabase.from("profiles").select("*").eq("id", session.user.id).single()
    .then(({ data }) => setProfile(data));
  }, [session]);

  const LANGUAGES = ["English", "Hindi", "Marathi", "Gujarati", "Bengali", "Odia", "Malayalam", "Tamil"];

  async function handleLookup(idOverride) {
  setError(""); setReport(null); setRecord(null);
  const id = (typeof idOverride === "string" ? idOverride : cardId).trim();
  if (!id) { setError("Enter a health card ID."); return; }
  setCardId(id);
  setLoadingRecord(true);
  try {
    setRecord(await getPatientRecord(id));
  } catch (e) { setError(e.message); }
  finally { setLoadingRecord(false); }
  }

  async function handleGenerate() {
    setError("");
    if (!symptoms.trim()) { setError("Enter current symptoms."); return; }
    setLoadingReport(true);
    try {
      const data = await generateReport(cardId.trim(), symptoms.trim());
      setReport(data.data);
      setTranslatedSummary(""); 
      setTranslatedReport(null); 
      setActiveLang("English");
    } catch (e) { setError(e.message); }
    finally { setLoadingReport(false); }
  }

  async function handleTranslate(lang) {
    setActiveLang(lang);
    if (lang === "English") { setTranslatedSummary(""); setTranslatedReport(null); return; }
    setTranslating(true);
    try {
      const [summary, fields] = await Promise.all([
        translateText(report.summary, lang),
        translateRecord({
          relevant_history: report.relevant_history || [],
          red_flags: report.red_flags || [],
          suggested_tests: report.suggested_tests || [],
          allergy_alerts: report.allergy_alerts || [],
          interaction_risks: (report.drug_interactions || []).map((d) => d.risk),
        }, lang),
      ]);
      setTranslatedSummary(summary);
      setTranslatedReport(fields);
    } catch (e) {
      setError(e.message);
    } finally {
      setTranslating(false);
    }
  }

  async function handleLogout() {
    await supabase.auth.signOut();
    setRecord(null); setReport(null); setCardId("");
  }

  if (authLoading) return <div className="login-wrap"><p>Loading…</p></div>;
  if (!session) return <Login />;

  // PATIENT VIEW: auto-load own record, read-only, no AI generation
  if (profile?.role === "patient") {
    return (
      <div className="app">
        <header className="topbar">
          <div className="brand">
            <span className="brand-mark">✚</span>

            <div>
              <h1>Saarthi</h1>
              <p>Continuity of Care · Patient View</p>
            </div>

            <button
              className="logout"
              onClick={handleLogout}
            >
              Sign out
            </button>
          </div>
        </header>

        <main className="container">
          <PatientView profile={profile} />
        </main>
      </div>
    );
  }

  return (
    
    <div className="app">
      {showScanner && (
        <QrScanner
          onScan={(text) => { setShowScanner(false); handleLookup(text); }}
          onClose={() => setShowScanner(false)}
        />
      )}
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">✚</span>

          <div>
            <h1>Saarthi</h1>
            <p>
              Continuity of Care · {profile?.role === "doctor"
                ? "Doctor Console"
                : "Patient View"}
            </p>
          </div>
          <nav className="topnav">
            <button
              className={view === "console" ? "navbtn active" : "navbtn"}
              onClick={() => setView("console")}
            >
              Patient Console
            </button>

            <button
              className={view === "surveillance" ? "navbtn active" : "navbtn"}
              onClick={() => setView("surveillance")}
            >
              Surveillance
            </button>
          </nav>

          <button
            className="logout"
            onClick={handleLogout}
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="container">
        {view === "surveillance" ? (
          <Surveillance />
        ) : (
          <>
            <section className="card">
              <label>Health Card ID</label>
              <div className="lookup-row">
                <input
                  value={cardId}
                  onChange={(e) => setCardId(e.target.value)}
                  placeholder="e.g. SHC-7K42-9QX"
                  onKeyDown={(e) => e.key === "Enter" && handleLookup()}
                />
                <button onClick={() => handleLookup()} disabled={loadingRecord}>
                  {loadingRecord ? "Looking up…" : "Look up record"}
                </button>

                <button
                  className="scan-btn"
                  onClick={() => setShowScanner(true)}
                >
                  Scan QR
                </button>
              </div>
              <p className="hint">In the live product, this comes from a QR scan.</p>
            </section>

            {error && <div className="error">{error}</div>}

            {record && (
              <section className="card">
                <div className="patient-head">
                  <div className="avatar">{(record.patient.full_name || "?").charAt(0)}</div>
                  <div>
                    <h2>{record.patient.full_name}</h2>
                    {record.patient.allergies && (
                      <div className="allergy-banner">
                        ⚠ Allergies: {record.patient.allergies}
                      </div>
                    )}
                    <p className="muted">
                      {record.patient.age} yrs · {record.patient.gender || "—"} · Blood {record.patient.blood_group || "—"}
                    </p>
                    <p className="cardid">{record.patient.health_card_id}</p>
                  </div>
                </div>

                <div className="cols">
                  <div>
                    <h3>Medical History</h3>
                    {record.medical_history.length === 0 && <p className="muted">No history on record.</p>}
                    {record.medical_history.map((h, i) => (
                      <div className="row-item" key={i}>
                        <strong>{h.disease_name}</strong>
                        <span className="muted">
                          {h.diagnosis_date || ""}{h.hospital_name ? ` · ${h.hospital_name}` : ""}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div>
                    <h3>Current Medications</h3>
                    {record.current_medications.length === 0 && <p className="muted">None recorded.</p>}
                    {record.current_medications.map((m, i) => (
                      <div className="row-item" key={i}>
                        <strong>{m.medicine_name}</strong>
                        <span className="muted">
                          {m.dosage || ""}{m.frequency ? ` · ${m.frequency}` : ""}{m.status ? ` · ${m.status}` : ""}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="generate">
                  <label>Current Symptoms</label>
                  <textarea
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                    placeholder="e.g. chest pain and shortness of breath"
                    rows={2}
                  />
                  <button className="primary" onClick={handleGenerate} disabled={loadingReport}>
                    {loadingReport ? "Generating…" : "Generate AI Report"}
                  </button>
                </div>
              </section>
            )}

            {record && <Timeline record={record} />}

            {report && (
              <section className="card">
                <div className="report-head">
                  <h2>AI Continuity-of-Care Report</h2>
                  <span className={`risk risk-${(report.risk_level || "LOW").toLowerCase()}`}>
                    Risk: {report.risk_level}
                  </span>
                </div>

                <div className="lang-row">
                  {LANGUAGES.map((lang) => (
                    <button
                      key={lang}
                      className={`lang-pill ${activeLang === lang ? "active" : ""}`}
                      onClick={() => handleTranslate(lang)}
                      disabled={translating}
                    >
                      {lang}
                    </button>
                  ))}
                </div>

                <p className="summary">
                  {translating
                    ? "Translating…"
                    : activeLang === "English"
                      ? report.summary
                      : translatedSummary || report.summary}
                </p>

                {report.drug_interactions?.length > 0 && (
                  <div className="alert">
                    <h4>⚠ Drug Interactions</h4>
                    {report.drug_interactions.map((d, i) => (
                      <p key={i}>
                        {Array.isArray(d.pair) ? d.pair.join(" + ") : ""} — {translatedReport?.interaction_risks?.[i] || d.risk}
                      </p>
                    ))}
                  </div>
                )}

                {report.allergy_alerts?.length > 0 && (
                  <div className="alert">
                    <h4>⚠ Allergy Alerts</h4>
                    {(translatedReport?.allergy_alerts || report.allergy_alerts).map((a, i) => <p key={i}>{a}</p>)}
                  </div>
                )}

                <div className="report-grid">
                  <ReportList title="Relevant History"
                    items={translatedReport?.relevant_history || report.relevant_history} />
                  <ReportList title="Red Flags"
                    items={translatedReport?.red_flags || report.red_flags} flag />
                  <ReportList title="Suggested Tests"
                    items={translatedReport?.suggested_tests || report.suggested_tests} />
                  <ReportList title="Current Medications"
                    items={report.current_medications} />  {/* deliberately NOT translated — drug names stay English */}
                </div>

                <p className="disclaimer">
                  AI-generated decision support for clinician review — not a diagnosis.
                </p>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

function ReportList({ title, items, flag }) {
  if (!items || items.length === 0) return null;
  return (
    <div className={`report-list ${flag ? "flag" : ""}`}>
      <h4>{title}</h4>
      <ul>{items.map((it, i) => <li key={i}>{it}</li>)}</ul>
    </div>
  );
}

function PatientView({ profile }) {
  const [record, setRecord] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!profile?.health_card_id) { setError("No health card linked to this account."); return; }
    getPatientRecord(profile.health_card_id).then(setRecord).catch((e) => setError(e.message));
  }, [profile]);

  if (error) return <div className="error">{error}</div>;
  if (!record) return <p className="muted">Loading your record…</p>;

  return (
    <section className="card">
      <div className="patient-head">
        <div className="avatar">{(record.patient.full_name || "?").charAt(0)}</div>
        <div>
          <h2>{record.patient.full_name}</h2>
          {record.patient.allergies && (
            <div className="allergy-banner">
              ⚠ Allergies: {record.patient.allergies}
            </div>
          )}
          <p className="muted">{record.patient.age} yrs · {record.patient.gender || "—"}</p>
          <p className="cardid">{record.patient.health_card_id}</p>
        </div>
      </div>
      <div className="cols">
        <div>
          <h3>Medical History</h3>
          {record.medical_history.map((h, i) => (
            <div className="row-item" key={i}>
              <strong>{h.disease_name}</strong>
              <span className="muted">
                {[h.diagnosis_date, h.hospital_name].filter(Boolean).join(" · ")}
              </span>
            </div>
          ))}
        </div>
        <div>
          <h3>Current Medications</h3>
          {record.current_medications.map((m, i) => (
            <div className="row-item" key={i}>
              <strong>{m.medicine_name}</strong>
              <span className="muted">{m.dosage || ""}{m.status ? ` · ${m.status}` : ""}</span>
            </div>
          ))}
        </div>
      </div>
      <p className="disclaimer">You can view your record. Only hospitals can add or edit entries.</p>
    </section>
  );
}

function Timeline({ record }) {
  // merge history + medications into one dated, sorted list
  const events = [];

  (record.medical_history || []).forEach((h) => {
    if (h.diagnosis_date) {
      events.push({
        date: h.diagnosis_date,
        type: "diagnosis",
        title: h.disease_name,
        detail: h.hospital_name || "",
      });
    }
  });

  (record.current_medications || []).forEach((m) => {
    events.push({
        date: m.start_date || m.created_at,
        type: "medication",
        title: `${m.medicine_name} started`,
        detail: [m.dosage, m.frequency].filter(Boolean).join(" · "),
    });
  });

  events.sort((a, b) => new Date(a.date) - new Date(b.date));

  if (events.length === 0) return null;

  return (
    <section className="card">
      <h3 style={{ marginBottom: 18 }}>Patient Medical Journey</h3>
      <div className="timeline">
        {events.map((e, i) => (
          <div className={`tl-item tl-${e.type}`} key={i}>
            <div className="tl-dot" />
            <div className="tl-content">
              <span className="tl-date">
                {new Date(e.date).toLocaleDateString("en-GB")}
              </span>
              <strong style={{ display: "block" }}>
                {e.title}
              </strong>
              {e.detail && <div className="muted">{e.detail}</div>}
              <span className="tl-tag">{e.type === "diagnosis" ? "DIAGNOSIS" : "MEDICATION"}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
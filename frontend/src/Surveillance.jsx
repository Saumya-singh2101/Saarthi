import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { getSurveillance } from "./api";

export default function Surveillance() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getSurveillance().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (!data) return <p className="muted">Loading surveillance data…</p>;

  const totals = Object.entries(data.settlement_totals || {})
    .sort((a, b) => b[1] - a[1]);

  return (
    <div className="surv">
      {data.synthetic && (
        <div className="synthetic-banner">
          Demonstration on synthetic data — detection algorithm is live; data is simulated.
        </div>
      )}

      <div className="surv-stats">
        <div className="stat-box">
          <span className="stat-num">{data.monitored_settlements}</span>
          <span className="stat-label">Settlements monitored</span>
        </div>
        <div className="stat-box">
          <span className="stat-num">{data.monitored_symptoms}</span>
          <span className="stat-label">Symptoms tracked</span>
        </div>
        <div className="stat-box alert-count">
          <span className="stat-num">{data.alerts.length}</span>
          <span className="stat-label">Active alerts</span>
        </div>
      </div>

      <h3 className="surv-h">Outbreak Alerts</h3>
      {data.alerts.length === 0 && <p className="muted">No anomalies detected.</p>}

      {data.alerts.map((a, i) => (
        <section className="card alert-card" key={i}>
          <div className="alert-card-head">
            <div>
              <span className={`sev sev-${a.severity.toLowerCase()}`}>{a.severity}</span>
              <h4>{a.symptom} spike — {a.settlement}</h4>
            </div>
            <div className="alert-metrics">
              <div><strong>{a.latest_count}</strong><span>today</span></div>
              <div><strong>{a.baseline_avg}</strong><span>avg</span></div>
              <div><strong>{a.z_score}σ</strong><span>z-score</span></div>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={a.trend} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eef0fb" />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#6b7280" }}
                     tickFormatter={(d) => d.slice(5)} />
              <YAxis tick={{ fontSize: 11, fill: "#6b7280" }} />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#dc2626" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>

          <p className="alert-note">
            {a.settlement} shows {a.latest_count} {a.symptom.toLowerCase()} cases today vs a
            baseline of {a.baseline_avg} — flagged for early review.
          </p>
        </section>
      ))}

      <h3 className="surv-h">Settlement Overview</h3>
      <section className="card">
        {totals.map(([name, total]) => {
          const max = totals[0][1] || 1;
          return (
            <div className="bar-row" key={name}>
              <span className="bar-label">{name}</span>
              <div className="bar-track">
                <div className="bar-fill" style={{ width: `${(total / max) * 100}%` }} />
              </div>
              <span className="bar-val">{total}</span>
            </div>
          );
        })}
      </section>
    </div>
  );
}
import { useState } from "react";
import { supabase } from "./supabase";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setError(""); setLoading(true);
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setError(error.message);
    setLoading(false);
    // on success, the auth listener in App.jsx swaps the screen automatically
  }

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="brand" style={{ justifyContent: "center", marginBottom: 20 }}>
          <span className="brand-mark">✚</span>
          <div><h1 style={{ color: "var(--primary-deep)" }}>Saarthi</h1></div>
        </div>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="doctor@saarthi.test" />
        <label style={{ marginTop: 12 }}>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
               onKeyDown={(e) => e.key === "Enter" && handleLogin()} />
        {error && <div className="error" style={{ marginTop: 14 }}>{error}</div>}
        <button className="primary" style={{ width: "100%", marginTop: 18 }}
                onClick={handleLogin} disabled={loading}>
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </div>
    </div>
  );
}
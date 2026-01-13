"use client";

import { useState } from "react";
import { API_URL } from "@/lib/api";

export default function ReportPage() {
  const [name, setName] = useState("");
  const [type, setType] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    const token = localStorage.getItem("access_token");
    console.log("TOKEN:", token);

    const res = await fetch(`${API_URL}/report/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        victim_name: name,
        classification: type,
      }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main style={{ maxWidth: 700, margin: "auto", paddingTop: 80 }}>
      <h1>Nueva Denuncia</h1>

      <input
        placeholder="Nombre de la persona denunciada"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{ width: "100%", padding: 10, marginTop: 10 }}
      />

      <input
        placeholder="Clasificación (fraud, harassment, etc.)"
        value={type}
        onChange={(e) => setType(e.target.value)}
        style={{ width: "100%", padding: 10, marginTop: 10 }}
      />

      <button onClick={submit} style={{ marginTop: 20 }}>
        {loading ? "Generando..." : "Generar reporte"}
      </button>

      {/* RESULTADO */}
      {result && (
        <section style={{ marginTop: 40 }}>
          <h2>Reporte generado</h2>
          <pre
            style={{
              background: "#111",
              padding: 20,
              borderRadius: 8,
              overflowX: "auto",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </section>
      )}
    </main>
  );
}

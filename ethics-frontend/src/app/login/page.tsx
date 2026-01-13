"use client";

import { useState } from "react";
import { API_URL } from "@/lib/api";
import { saveToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState<1 | 2>(1);
  const router = useRouter();

  const handleLogin = async () => {
    try {
      // 🔹 PASO 1: username + password
      if (step === 1) {
        const res = await fetch(`${API_URL}/auth/login/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        const data = await res.json();
        console.log(data);

        if (!res.ok) {
          alert(data.detail || "Error al iniciar sesión");
          return;
        }

        // 👉 OTP enviado
        setStep(2);
        return;
      }

      // 🔹 PASO 2: verificar OTP
      const res = await fetch(`${API_URL}/auth/verify/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, otp }),
      });

      const data = await res.json();
      console.log("info",data);

      if (!res.ok) {
        alert(data.detail || "Código inválido");
        return;
      }

      // ✅ Guardar JWT
      saveToken(data.access);
      router.push("/report");

    } catch (error) {
      console.error("Login error:", error);
      alert("Error de conexión");
    }
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Login</h1>

      <input
        className="w-full p-2 bg-gray-900 rounded"
        placeholder="Usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      {step === 1 && (
        <input
          className="w-full p-2 bg-gray-900 rounded"
          placeholder="Contraseña"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      )}

      {step === 2 && (
        <input
          className="w-full p-2 bg-gray-900 rounded"
          placeholder="Código OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />
      )}

      <button
        onClick={handleLogin}
        className="w-full bg-white text-black py-2 rounded"
      >
        {step === 1 ? "Enviar código" : "Verificar y entrar"}
      </button>

      <p className="text-sm text-gray-400">
        ¿No tienes cuenta? <a href="/register">Regístrate</a>
      </p>
    </div>
  );
}

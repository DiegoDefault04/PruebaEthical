"use client";

import { useState } from "react";
import { API_URL } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const router = useRouter();

  const handleRegister = async () => {
    await fetch(`${API_URL}/auth/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, phone }),
    });

    alert("Usuario creado");
    router.push("/");
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Registro</h1>

      <input className="w-full p-2 bg-gray-900 rounded" placeholder="Usuario" onChange={(e) => setUsername(e.target.value)} />
      <input className="w-full p-2 bg-gray-900 rounded" placeholder="Contraseña" type="password" onChange={(e) => setPassword(e.target.value)} />
      <input className="w-full p-2 bg-gray-900 rounded" placeholder="Teléfono" onChange={(e) => setPhone(e.target.value)} />
      <input className="w-full p-2 bg-gray-900 rounded" placeholder="Correo electrónico" type="email" onChange={(e) => setEmail(e.target.value)} />
      <button onClick={handleRegister} className="w-full bg-white text-black py-2 rounded">
        Registrar
      </button>
    </div>
  );
}

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
import requests
import os
import re

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta2/models/"
    f"text-bison-001:generateText?key={GOOGLE_API_KEY}"
)

# =========================
# UTILIDADES
# =========================
GENERIC_PATTERNS = [
    r"posible",
    r"podr[ií]a",
    r"incumplimiento",
    r"pol[ií]ticas",
    r"se identificaron",
]


def is_generic(text: str) -> bool:
    if not text:
        return True
    return any(re.search(p, text.lower()) for p in GENERIC_PATTERNS)


def call_gemini(prompt, temperature=0.9, max_tokens=250):
    try:
        response = requests.post(
            GEMINI_URL,
            json={
                "prompt": {"text": prompt},
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
            timeout=30,
        )
        data = response.json()
        return data.get("candidates", [{}])[0].get("output", "").strip()
    except Exception:
        return None


def generate_story(prompt):
    for temp in (0.7, 0.9, 1.0):
        text = call_gemini(prompt, temperature=temp)
        if text and not is_generic(text):
            return text
    return None


# =========================
# FALLBACKS POR CLASIFICACIÓN
# =========================
INCIDENT_FALLBACKS = {
    "fraude_en_nomina": (
        "Se detectó la creación de registros de empleados inexistentes y "
        "la autorización de pagos duplicados en el sistema de nómina sin justificación operativa."
    ),
    "fraude": (
        "Se realizaron operaciones financieras sin respaldo documental y "
        "aprobaciones fuera de los procesos establecidos."
    ),
    "hostigamiento_laboral": (
        "El superior jerárquico realizó comentarios despectivos de forma reiterada, "
        "asignó cargas laborales excesivas y ejerció presión indebida sobre el personal."
    ),
    "conflicto_de_interes": (
        "La persona denunciada participó en decisiones comerciales favoreciendo a un proveedor "
        "con el que mantiene una relación personal no declarada."
    ),
}

EVIDENCE_FALLBACKS = {
    "fraude_en_nomina": (
        "Existen recibos de nómina, registros del sistema de recursos humanos y "
        "bitácoras de pagos que evidencian los movimientos irregulares."
    ),
    "fraude": (
        "Se cuenta con registros contables, comprobantes de transferencia y "
        "correos electrónicos relacionados con las operaciones cuestionadas."
    ),
    "hostigamiento_laboral": (
        "Se tienen mensajes internos, correos electrónicos y reportes del área "
        "que documentan las conductas reportadas."
    ),
    "conflicto_de_interes": (
        "Existen contratos, correos electrónicos y registros de proveedores "
        "que demuestran la relación no declarada."
    ),
}


class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        victim_name = request.data.get("victim_name")
        classification_raw = request.data.get("classification", "").lower()
        position = request.data.get("position", "Empleado")
        department = request.data.get("department", "General")

        if not victim_name or not classification_raw:
            return Response(
                {"error": "victim_name y classification son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        classification_key = classification_raw.replace(" ", "_")

        # =========================
        # PROMPTS DINÁMICOS
        # =========================
        incident_prompt = f"""
Inventa una historia REALISTA y ESPECÍFICA relacionada con:
"{classification_raw}"

Contexto:
- Empresa privada en México
- Lenguaje profesional
- Hechos concretos

Reglas:
- Describe acciones reales relacionadas con el tipo de denuncia.
- No uses lenguaje genérico ni legal.
- No menciones políticas ni investigaciones futuras.
- Máximo 4 oraciones.

Responde solo con la historia.
"""

        evidence_prompt = f"""
Inventa evidencia CONCRETA que respalde una denuncia de:
"{classification_raw}"

Reglas:
- Menciona documentos, registros o comunicaciones reales.
- Usa al menos dos tipos de evidencia.
- No uses texto genérico.
- Máximo 2 oraciones.

Responde solo con la evidencia.
"""

        incident_text = generate_story(incident_prompt)
        evidence_text = generate_story(evidence_prompt)

        # =========================
        # FALLBACK CORRECTO (POR TIPO)
        # =========================
        if not incident_text:
            incident_text = INCIDENT_FALLBACKS.get(
                classification_key,
                "Se reportó una conducta irregular relacionada con las funciones del puesto."
            )

        if not evidence_text:
            evidence_text = EVIDENCE_FALLBACKS.get(
                classification_key,
                "Existen documentos internos y comunicaciones que respaldan la denuncia."
            )

        return Response({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "anonymous": True,
            "channel": "web",

            "reporter": {
                "relationship_to_company": "employee",
                "country": "México"
            },

            "people": {
                "offender": {
                    "name": victim_name,
                    "position": position,
                    "department": department
                }
            },

            "incident": {
                "type": classification_raw,
                "description": incident_text,
                "approximate_date": datetime.now().strftime("%Y-%m"),
                "is_ongoing": True
            },

            "location": {
                "city": "Ciudad de México",
                "work_related": True
            },

            "evidence": {
                "has_evidence": True,
                "description": evidence_text
            }
        })

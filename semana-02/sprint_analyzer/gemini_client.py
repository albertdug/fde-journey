import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def analyze_sprint(sprint_summary: str) -> str:
    """Llama a Gemini para analizar el sprint y generar recomendaciones."""

    prompt = f"""Eres un experto Agile Coach analizando datos de sprint.

Datos del sprint:
{sprint_summary}

Proporciona:
1. Una evaluación breve del sprint (2-3 oraciones)
2. El principal riesgo identificado
3. Una recomendación concreta para el próximo sprint

Responde en español, de forma concisa y accionable."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300}
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

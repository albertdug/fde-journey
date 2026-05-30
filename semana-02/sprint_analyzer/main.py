import asyncio
from datetime import datetime
from models import Sprint, Story
from gemini_client import analyze_sprint

# Datos mock — reemplazalos con datos reales de tu trabajo si tenés
def create_sample_sprints() -> list[Sprint]:
    return [
        Sprint(
            number=41,
            team_name="Equipo Alpha",
            start_date=datetime(2024, 1, 8),
            end_date=datetime(2024, 1, 19),
            committed_points=40,
            stories=[
                Story("US-101", "Login con SSO", 8, "done"),
                Story("US-102", "Dashboard principal", 13, "done"),
                Story("US-103", "Notificaciones email", 5, "done"),
                Story("US-104", "Reportes PDF", 8, "in_progress"),
                Story("US-105", "API mobile", 6, "not_started"),
            ]
        ),
        Sprint(
            number=42,
            team_name="Equipo Alpha",
            start_date=datetime(2024, 1, 22),
            end_date=datetime(2024, 2, 2),
            committed_points=35,
            stories=[
                Story("US-104", "Reportes PDF", 8, "done"),
                Story("US-106", "Búsqueda avanzada", 13, "done"),
                Story("US-107", "Exportar CSV", 5, "done"),
                Story("US-108", "Integración Slack", 9, "done"),
            ]
        ),
    ]

async def main():
    sprints = create_sample_sprints()

    print("=== AGILE SPRINT ANALYZER ===\n")

    for sprint in sprints:
        print(sprint.summary())
        print()

    # Análisis con Gemini del sprint más reciente
    latest = sprints[-1]
    print("=== ANÁLISIS IA (Gemini) ===\n")
    print("Analizando con Gemini...")

    try:
        analysis = await analyze_sprint(latest.summary())
        print(analysis)
    except Exception as e:
        print(f"Error llamando a Gemini: {e}")
        print("(Verificá que GEMINI_API_KEY esté en tu .env)")

asyncio.run(main())
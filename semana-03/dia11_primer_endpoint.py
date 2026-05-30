from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

# FastAPI crea la app — acá va toda la configuración
app = FastAPI(
    title="Agile Metrics API",
    description="API para gestionar métricas de sprints y equipos",
    version="0.1.0"
)

# Pydantic define la forma de los datos
class SprintResponse(BaseModel):
    sprint_number: int
    team_name: str
    velocity: int
    completion_rate: float
    created_at: datetime

# GET simple — sin parámetros
@app.get("/")
def root():
    return {"message": "Agile Metrics API", "status": "running"}

# GET con respuesta tipada
@app.get("/sprints/latest", response_model=SprintResponse)
def get_latest_sprint():
    # Datos hardcodeados por ahora — en semana 4 vendrán de la DB
    return SprintResponse(
        sprint_number=42,
        team_name="Equipo Alpha",
        velocity=35,
        completion_rate=87.5,
        created_at=datetime.now()
    )

# GET que devuelve una lista
@app.get("/sprints")
def list_sprints():
    return [
        {"sprint_number": 41, "velocity": 28, "team": "Alpha"},
        {"sprint_number": 42, "velocity": 35, "team": "Alpha"},
        {"sprint_number": 40, "velocity": 22, "team": "Beta"},
    ]
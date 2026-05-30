from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, validator
from typing import Optional
from enum import Enum

app = FastAPI(title="Agile Metrics API v2")

class TeamStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    on_hold = "on_hold"

class SprintCreate(BaseModel):
    sprint_number: int
    team_name: str
    committed_points: int
    completed_points: int

    @validator('completed_points')
    def completed_cannot_exceed_committed(cls, v, values):
        if 'committed_points' in values and v > values['committed_points'] * 1.2:
            raise ValueError('Los puntos completados no pueden exceder en más de 20% los comprometidos')
        return v

    @property
    def completion_rate(self) -> float:
        if self.committed_points == 0:
            return 0.0
        return round(self.completed_points / self.committed_points * 100, 1)

# PATH PARAMETER — parte de la URL
# GET /sprints/42
@app.get("/sprints/{sprint_number}")
def get_sprint(sprint_number: int):
    # FastAPI valida automáticamente que sprint_number sea int
    if sprint_number < 1:
        raise HTTPException(status_code=400, detail="El número de sprint debe ser mayor a 0")
    if sprint_number > 100:
        raise HTTPException(status_code=404, detail=f"Sprint {sprint_number} no encontrado")
    return {"sprint_number": sprint_number, "velocity": sprint_number * 2}

# QUERY PARAMETERS — después del ?
# GET /teams?status=active&limit=10&offset=0
@app.get("/teams")
def list_teams(
    status: Optional[TeamStatus] = None,       # Enum con validación automática
    limit: int = Query(default=10, ge=1, le=100),  # entre 1 y 100
    offset: int = Query(default=0, ge=0),
    search: Optional[str] = None
):
    teams = [
        {"name": "Alpha", "status": "active", "velocity_avg": 34},
        {"name": "Beta", "status": "active", "velocity_avg": 28},
        {"name": "Gamma", "status": "inactive", "velocity_avg": 15},
        {"name": "Delta", "status": "on_hold", "velocity_avg": 20},
    ]

    # Filtrar por status si se especifica
    if status:
        teams = [t for t in teams if t["status"] == status.value]

    # Filtrar por búsqueda
    if search:
        teams = [t for t in teams if search.lower() in t["name"].lower()]

    return {
        "total": len(teams),
        "limit": limit,
        "offset": offset,
        "items": teams[offset:offset + limit]
    }

# REQUEST BODY — datos en el cuerpo del POST
@app.post("/sprints", status_code=201)
def create_sprint(sprint: SprintCreate):
    # Pydantic ya validó los datos antes de llegar acá
    return {
        "message": "Sprint creado exitosamente",
        "sprint_number": sprint.sprint_number,
        "completion_rate": sprint.completion_rate,
        "status": "created"
    }
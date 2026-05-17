from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel, field_validator

# Dataclass - para datos somples internos 
@dataclass
class SprintMetrics:
    sprint_number: int
    velocity: int
    team_name: str
    complete_at: datetime = field(default_factory=datetime.now)
    stories_completed: list[str] = field(default_factory=list)

    def velocity_trend(self, previous_velocity: int) -> str:
        diff = self.velocity - previous_velocity
        if diff > 0:
            return f"↑ ={diff} puntos"
        elif diff < 0:
            return f"↓ ={abs(diff)} puntos"
        else:
            return "La velocidad se mantiene igual"

# PYDANTIC -  para datos que vienen de fuentes externas - validacion y parsing(APIs, json, formularios)
class SprintInput(BaseModel):
    sprint_number: int
    velocity: int
    team_name: str

    @field_validator('velocity')
    @classmethod
    def velocity_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('La velocidad debe ser un número positivo')
        return v
    
    @field_validator('team_name')
    @classmethod
    def team_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre del equipo no puede estar vacío')
        return v.strip()
    

# Probando dataclass
sprint = SprintMetrics(
    sprint_number=42, 
    velocity=35, 
    team_name="Equipo Alpha",
    stories_completed=["Historia 1", "Historia 2", "Historia 3"]
)
print(f"Sprint: {sprint.sprint_number}, Velocidad: {sprint.velocity}")

# Probando Pydantic - datos validos
try:
    input_valido = SprintInput(sprint_number=1, velocity=28, team_name=" Equipo Beta ")
    print(f"Input válido: {input_valido}")
except Exception as e:
        print(f"Error en input válido: {e}")

# Probando Pydantic - datos invalidos
try:
    input_invalido = SprintInput(sprint_number=2, velocity=5, team_name=" ")
    print(f"Esto no deberia imprimirse")
except Exception as e:
        print(f"Error esperado {e}")
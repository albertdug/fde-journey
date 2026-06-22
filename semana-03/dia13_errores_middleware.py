from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
import logging

# Configurar logging estructurado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agile Metrics API v3")

# CORS — necesario cuando el frontend está en otro dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # en producción: tu dominio real
    allow_methods=["*"],
    allow_headers=["*"],
)

# MIDDLEWARE DE LOGGING — se ejecuta en cada request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Generar ID único para rastrear el request
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    logger.info(f"[{request_id}] → {request.method} {request.url.path}")

    response = await call_next(request)

    duration = round((time.time() - start_time) * 1000, 2)
    logger.info(f"[{request_id}] ← {response.status_code} ({duration}ms)")

    # Agregar el request_id en los headers de respuesta
    response.headers["X-Request-ID"] = request_id
    return response

# EXCEPCIONES PERSONALIZADAS
class SprintNotFoundError(Exception):
    def __init__(self, sprint_number: int):
        self.sprint_number = sprint_number

class TeamCapacityError(Exception):
    def __init__(self, message: str):
        self.message = message

# HANDLERS DE EXCEPCIONES — centralizan el manejo de errores
@app.exception_handler(SprintNotFoundError)
async def sprint_not_found_handler(request: Request, exc: SprintNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "sprint_not_found",
            "message": f"El sprint {exc.sprint_number} no existe",
            "hint": "Verificá el número de sprint o consultá GET /sprints para ver los disponibles"
        }
    )

@app.exception_handler(TeamCapacityError)
async def team_capacity_handler(request: Request, exc: TeamCapacityError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "capacity_validation_error",
            "message": exc.message
        }
    )

# Endpoints que usan las excepciones personalizadas
@app.get("/sprints/{sprint_number}")
def get_sprint(sprint_number: int):
    sprints_db = {41: {"velocity": 28}, 42: {"velocity": 35}}
    if sprint_number not in sprints_db:
        raise SprintNotFoundError(sprint_number)
    return {"sprint_number": sprint_number, **sprints_db[sprint_number]}

@app.post("/capacity/validate")
def validate_capacity(team_size: int, sprint_days: int, focus_factor: float = 0.7):
    if team_size <= 0:
        raise TeamCapacityError("El tamaño del equipo debe ser mayor a 0")
    if sprint_days <= 0 or sprint_days > 30:
        raise TeamCapacityError("Los días de sprint deben estar entre 1 y 30")
    if not 0.1 <= focus_factor <= 1.0:
        raise TeamCapacityError("El focus factor debe estar entre 0.1 y 1.0")

    capacity = team_size * sprint_days * focus_factor * 8  # horas
    return {
        "team_size": team_size,
        "sprint_days": sprint_days,
        "focus_factor": focus_factor,
        "capacity_hours": round(capacity, 1),
        "capacity_points_estimate": round(capacity / 4, 0)  # asumiendo 4h/punto
    }
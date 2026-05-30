import os
from pathlib import Path

# Cargar variables del archivo .env manualmente
def load_env_file(env_path: Path):
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env_file(Path(__file__).parent / ".env")

# Patrón recomendado: fallar rápido si falta una variable crítica
def get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variable de entorno requerida no encontrada: {key}")
    return value

def get_optional_env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

# Config centralizada
class Config:
    github_token: str = get_required_env("GITHUB_TOKEN")
    app_name: str = get_optional_env("APP_NAME", "app")
    environment: str = get_optional_env("ENVIRONMENT", "development")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

config = Config()
print(f"App: {config.app_name} ({config.environment})")
print(f"¿Producción?: {config.is_production}")
import asyncio
import httpx
from typing import Optional

# Error handling de producción — no solo try/except genérico

class APIError(Exception):
    """Error al llamar una API externa"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 0.5
) -> dict:
    """
    Fetch con retry automático y backoff exponencial.
    Patrón estándar para llamadas a APIs externas en producción.
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)

                if response.status_code == 429:  # rate limit
                    wait = backoff_factor * (2 ** attempt)
                    print(f"Rate limit. Esperando {wait}s antes del intento {attempt + 2}")
                    await asyncio.sleep(wait)
                    continue

                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException:
            last_error = APIError(f"Timeout en intento {attempt + 1}")
            wait = backoff_factor * (2 ** attempt)
            await asyncio.sleep(wait)

        except httpx.HTTPStatusError as e:
            raise APIError(
                f"HTTP {e.response.status_code}: {e.response.text[:100]}",
                status_code=e.response.status_code
            )

    raise APIError(f"Falló después de {max_retries} intentos") from last_error

async def main():
    # URL válida
    try:
        data = await fetch_with_retry("https://api.github.com/users/torvalds")
        print(f"OK: {data['login']}")
    except APIError as e:
        print(f"Error: {e}")

    # URL inválida — verás el manejo de error
    try:
        data = await fetch_with_retry("https://httpbin.org/status/404")
    except APIError as e:
        print(f"Error esperado: {e} (status: {e.status_code})")

asyncio.run(main())
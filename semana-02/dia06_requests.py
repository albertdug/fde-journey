import asyncio
import httpx  # versión moderna y async de requests

# Instalá primero:
# uv pip install httpx

async def get_github_user(username: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}",
            timeout=10.0
        )
        response.raise_for_status()  # lanza excepción si status >= 400
        return response.json()

async def get_public_repos(username: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 5, "sort": "updated"},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()

async def main():
    username = "torvalds"  # cambialo por cualquier usuario de GitHub

    # Llamadas en paralelo
    user, repos = await asyncio.gather(
        get_github_user(username),
        get_public_repos(username)
    )

    print(f"Usuario: {user['name']}")
    print(f"Bio: {user.get('bio', 'Sin bio')}")
    print(f"Repos públicos: {user['public_repos']}")
    print(f"\nÚltimos 5 repos:")
    for repo in repos:
        print(f"  - {repo['name']}: {repo.get('description', 'Sin descripción')[:50]}")

asyncio.run(main())
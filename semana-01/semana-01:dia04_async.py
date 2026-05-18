import asyncio
import time

# Sincrono - hace una tarea a la vez
def tarea_sincrona(nombre: str, segundos: int) -> str:
    print(f"  Iniciando {nombre} ...")
    time.sleep(segundos) # simula trabajo (llamada a API, DB, etc)
    print(f" {nombre} termino.")
    return f"Resultado de {nombre}"

# Asincrono - permite hacer varias tareas al mismo tiempo
async def tarea_asincrona(nombre: str, segundos: int) -> str:
    print(f"  Iniciando {nombre} ...")
    await asyncio.sleep(segundos) # simula el hilo mientras espera 
    print(f" {nombre} termino.")
    return f"Resultado de {nombre}"

# Comparacion
print("=== Sincrono === ")
inicio = time.time()
tarea_sincrona("Sprint Report", 2)
tarea_sincrona("Team Metrics", 2) 
tarea_sincrona("Velocity Chart", 2)
print(f"Total: {time.time() - inicio:.1f}s\n") # -6 segundos

print("=== Asincrono === ")
async def main():
    inicio = time.time()
    # gather ejecuta las tareas al mismo tiempo
    resultados = await asyncio.gather(
        tarea_asincrona("Sprint Report", 2),
        tarea_asincrona("Team Metrics", 2),
        tarea_asincrona("Velocity Chart", 2)
    )
    print(f"Resultados: {resultados}")
    print(f"Total: {time.time() - inicio:.1f}s") # -2 segundos

asyncio.run(main())
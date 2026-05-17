#Type hints - nuevos desde Python 3.5, estandar desde Python 3.10

def saludar(nombre: str, veces: int = 1) -> str:
    return f"Hola, {nombre}!" * veces
#print(saludar("Mundo", 3))

# f-strings - reemplaza format() a %
nombre = "Albert"
edad = 37
print(f"{nombre} tiene {edad} años")

# Walrus operatos := - asigna y evalua una linea
numeros = [1, 2, 3, 4,5,6,7]
if (n := len(numeros)) > 5:
    print(f"La lista tiene {n} elementos que son mas que 5")

# List of comprehensions con condicion
pares = [x for x in range(20) if x % 2 == 0]
print(f"Números pares: {pares}")

# Dict comprehensions
cuadrados = {x: x**2 for x in range(1, 6)}
print(f"Cuadrados: {cuadrados}")

# Unpacking moderno
primero, *resto = [1, 2, 3, 4, 5]
print(f"Primero: {primero}, Resto: {resto}")

#Match statement - nuevo desde Python 3.10 - como switch case pero mas potente
def clasificar_sprint(velocity: int) -> str:
    match velocity:
        case v if v < 20:
            return "bajo, sigue asi"
        case v if v < 40:
            return "normal revisa si tienes cuellos de botella o estas esperando mucho en alguna columna"
        case _:
            return "Alto comienza a revisar flow metrics para entender mejor tu proceso"
        
print(clasificar_sprint(15))

# Percentil 85 con nuevo valor
from statistics import quantiles
from typing import Union

def agregar_valor_y_calcular_percentil85(
    nuevo_valor: Union[int, float], 
    lista_existente: list[Union[int, float]]
) -> tuple[Union[int, float], list[Union[int, float]]]:
    """
    Agrega un nuevo valor a la lista y calcula el percentil 85.
    
    Args:
        nuevo_valor: valor numérico a agregar
        lista_existente: lista con valores anteriores
    
    Returns:
        tupla con (percentil_85, lista_actualizada)
    """
    lista_actualizada = lista_existente + [nuevo_valor]
    # quantiles divide en 100 partes, el índice 84 es el percentil 85
    percentil_85 = quantiles(lista_actualizada, n=100)[84]
    return percentil_85, lista_actualizada

# Ejemplo de uso
valores = [10, 20, 30, 40, 50, 60, 70, 80, 90]
nuevo = 95
p85, lista_nueva = agregar_valor_y_calcular_percentil85(nuevo, valores)
print(f"Percentil 85 después de agregar {nuevo}: {p85}")
print(f"Lista actualizada: {lista_nueva}")


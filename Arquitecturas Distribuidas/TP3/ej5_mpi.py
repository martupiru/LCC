from mpi4py import MPI
import time
import math

# ---------- Función para verificar si un número es primo ----------
def es_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    raiz = int(math.sqrt(n)) + 1
    for i in range(3, raiz, 2):
        if n % i == 0:
            return False
    return True

# ---------- Inicialización MPI ----------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ---------- Rank 0 pide el número N ----------
if rank == 0:
    N = int(input("Ingrese el número N: "))
    t0 = time.time()
else:
    N = None

# Enviar N a todos
N = comm.bcast(N, root=0)

# ---------- Calcular el subrango de cada proceso ----------
chunk = N // size
inicio = rank * chunk
fin = (rank + 1) * chunk if rank != size - 1 else N

# Ajustar para que el rango empiece en al menos 2
if inicio < 2:
    inicio = 2

# ---------- Calcular primos en el subrango ----------
primos_local = [n for n in range(inicio, fin) if es_primo(n)]

# ---------- Reunir resultados en el root ----------
primos_todos = comm.gather(primos_local, root=0)

if rank == 0:
    # Unir todas las listas
    primos_totales = []
    for sublista in primos_todos:
        primos_totales.extend(sublista)

    primos_totales.sort()
    cantidad = len(primos_totales)
    mayores_10 = primos_totales[-10:] if cantidad >= 10 else primos_totales

    t1 = time.time()
    elapsed = t1 - t0

    # ---------- Mostrar resultados ----------
    print("\n===== RESULTADOS MPI =====")
    print(f"Cantidad total de primos menores que {N}: {cantidad}")
    print(f"Los 10 mayores primos son: {mayores_10}")
    print(f"Tiempo total = {elapsed:.4f} segundos")
    print("Para speedup: Speedup = T1 / T(size)")

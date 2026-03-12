from mpi4py import MPI
import time

def count_overlapping(text, pattern):
    """Cuenta apariciones (incluyendo solapadas) de un patrón en un texto."""
    if not pattern:
        return 0
    count = start = 0
    while True:
        idx = text.find(pattern, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1  # Permite solapamiento
    return count

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

texto = None
patrones = None

if rank == 0:
    # Leer texto y patrones solo en el proceso root
    with open("texto.txt", "r", encoding="utf-8", errors="ignore") as f:
        texto = f.read()

    with open("patrones.txt", "r", encoding="utf-8", errors="ignore") as f:
        patrones = [line.strip() for line in f.readlines()]

    # Rellenar lista de patrones si hay menos que procesos
    if size > len(patrones):
        patrones += [""] * (size - len(patrones))
    else:
        patrones = patrones[:size]

    t0 = time.time()

# Enviar texto a todos los procesos
texto = comm.bcast(texto, root=0)

# Repartir patrones
mi_patron = comm.scatter(patrones, root=0)

# Contar apariciones
mi_conteo = count_overlapping(texto, mi_patron)

# Recolectar resultados
conteos = comm.gather(mi_conteo, root=0)

if rank == 0:
    t1 = time.time()
    elapsed = t1 - t0

    # Mostrar resultados
    for i, c in enumerate(conteos):
        print(f"el patron {i} aparece {c} veces.")

    print(f"\nTiempo total (MPI size={size}): {elapsed:.6f} segundos")
    print("Para calcular speedup: T1 / T(size)")

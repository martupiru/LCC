from mpi4py import MPI
import numpy as np
import time
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ----- Configuración -----
if rank == 0:
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
else:
    N = None

N = comm.bcast(N, root=0)

# Dividir filas entre procesos
rows_per_proc = N // size
extra = N % size
if rank < extra:
    start = rank * (rows_per_proc + 1)
    end = start + rows_per_proc + 1
else:
    start = extra * (rows_per_proc + 1) + (rank - extra) * rows_per_proc
    end = start + rows_per_proc
local_rows = end - start

# ----- Crear / distribuir matrices -----
if rank == 0:
    A = np.full((N, N), 0.1, dtype=np.float32)
    B = np.full((N, N), 0.2, dtype=np.float32)
else:
    A = None
    B = None

# Enviar B completa a todos
B = comm.bcast(B, root=0)

# Enviar porciones de A
if rank == 0:
    for r in range(1, size):
        if r < extra:
            s = r * (rows_per_proc + 1)
            e = s + (rows_per_proc + 1)
        else:
            s = extra * (rows_per_proc + 1) + (r - extra) * rows_per_proc
            e = s + rows_per_proc
        comm.Send([A[s:e, :], MPI.FLOAT], dest=r)
    A_local = A[start:end, :]
else:
    A_local = np.empty((local_rows, N), dtype=np.float32)
    comm.Recv([A_local, MPI.FLOAT], source=0)

# ----- Calcular -----
if rank == 0:
    t0 = time.time()

C_local = np.matmul(A_local, B)
local_sum = np.sum(C_local, dtype=np.float64)

# Enviar resultados
if rank == 0:
    C = np.empty((N, N), dtype=np.float32)
    C[start:end, :] = C_local
    for r in range(1, size):
        if r < extra:
            s = r * (rows_per_proc + 1)
            e = s + (rows_per_proc + 1)
        else:
            s = extra * (rows_per_proc + 1) + (r - extra) * rows_per_proc
            e = s + rows_per_proc
        temp = np.empty((e - s, N), dtype=np.float32)
        comm.Recv([temp, MPI.FLOAT], source=r)
        C[s:e, :] = temp
else:
    comm.Send([C_local, MPI.FLOAT], dest=0)

total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

if rank == 0:
    t1 = time.time()
    elapsed = t1 - t0

    print(f"C[0][0] = {C[0,0]:.4f}    C[0][{N-1}] = {C[0,N-1]:.4f}")
    print(f"C[{N-1}][0] = {C[N-1,0]:.4f}    C[{N-1}][{N-1}] = {C[N-1,N-1]:.4f}")
    print(f"Suma total = {total_sum:.6f}")
    print(f"N = {N}, size={size}, Tiempo total = {elapsed:.6f} s")
    print("Speedup = T1 / T(size)")

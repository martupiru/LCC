from mpi4py import MPI
import time
import math  # para comparar con math.log

def taylor_ln(x, start, end):
    # ln(x) = 2 * sum_{n=start}^{end-1} (1/(2n+1)) * y^(2n+1)
    y = (x - 1.0) / (x + 1.0)
    s = 0.0
    # OJO: range(end) itera hasta end-1, está bien
    for n in range(start, end):
        power = y ** (2*n + 1)
        term = (1.0 / (2*n + 1)) * power
        s += term
    return 2.0 * s

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

x = 1500000.0
N_TERMS = 10_000_000  # diez millones

# dividir carga
base = N_TERMS // size
start = rank * base
end = start + base
if rank == size - 1:
    end = N_TERMS  # último proceso se queda con el resto

# medir tiempo de cómputo total (solo rank 0 inicia el cronómetro)
if rank == 0:
    t0 = time.time()

partial_sum = taylor_ln(x, start, end)

# reducir suma parcial al root
total_sum = comm.reduce(partial_sum, op=MPI.SUM, root=0)

if rank == 0:
    t1 = time.time()
    approx = total_sum
    elapsed = t1 - t0

    print(f"[MPI size={size}] ln({x}) ≈ {approx:.15f}")
    print(f"math.log({x}) = {math.log(x):.15f}  (para comparar)")
    print(f"Tiempo total = {elapsed:.6f} segundos")
    # Después ustedes con los apuntes:
    # speedup = (tiempo con 1 proceso) / (tiempo con size procesos)

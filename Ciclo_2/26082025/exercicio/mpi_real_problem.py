#!/usr/bin/python3
"""
mpi_real_problem.py - Resolução distribuída de sistema linear com SciPy
"""

from mpi4py import MPI
import numpy as np
from scipy.linalg import solve
import time

def simulate_system(rank, size):
    """Cada nó resolve parte do sistema linear Ax=b"""
    N = 1000
    np.random.seed(rank)
    
    # Criar sistema linear
    A = np.random.rand(N, N)
    b = np.random.rand(N)

    # Simulação de computação pesada
    start = time.time()
    x = solve(A, b)  # Resolver sistema linear
    duration = time.time() - start

    return duration, np.sum(x)  # Retornar soma como estatística

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"[Rank {rank}/{size}] iniciando cálculo distribuído")

    duration, stat = simulate_system(rank, size)

    all_results = comm.gather((rank, duration, stat), root=0)

    if rank == 0:
        print("\n=== Resultados Agregados ===")
        for r, dur, s in all_results:
            print(f"Rank {r}: tempo={dur:.3f}s, soma={s:.3f}")

if __name__ == "__main__":
    main()


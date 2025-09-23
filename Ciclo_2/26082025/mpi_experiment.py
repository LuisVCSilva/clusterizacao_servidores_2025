#!/usr/bin/python3
"""
Exemplo de experimento MPI distribuído
para rodar dentro de hosts do Mininet
"""

from mpi4py import MPI
import time
import random

def simulate_computation():
    """
    Simula uma carga de trabalho em cada nó.
    Retorna o tempo gasto e uma estatística qualquer.
    """
    start = time.time()
    # Simular cálculo com loop -- fazer com exemplo real -- integracao monte carlo ou runge kutta, inventar problema
    total = 0
    for i in range(1_000_000):
        total += random.randint(0, 10)
    end = time.time()
    return end - start, total

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"[Host rank {rank}/{size}] Iniciando experimento MPI")

    # Simulação de cálculo
    duration, result = simulate_computation()
    print(f"[Rank {rank}] Computation done in {duration:.3f}s, result={result}")

    # Coletar resultados de todos os nós no rank 0
    all_results = comm.gather((rank, duration, result), root=0)

    if rank == 0:
        print("\n=== Resultados agregados ===")
        for r, dur, res in all_results:
            print(f"Rank {r}: tempo={dur:.3f}s, resultado={res}")

if __name__ == "__main__":
    main()

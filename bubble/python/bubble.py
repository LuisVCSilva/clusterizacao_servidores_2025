from mpi4py import MPI
import numpy as np
import time

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 128  # Altere para 32, 64, 128 ou 256

local_n = N // size
local_data = np.empty(local_n, dtype='i')

if rank == 0:
    data = np.random.randint(0, 100, size=N, dtype='i')
    print("Vetor original:", data)
else:
    data = None

comm.Scatter(data, local_data, root=0)

print(f"[Rank {rank}] Antes da ordenação: {local_data}")

start_time = time.time()

bubble_sort(local_data)

print(f"[Rank {rank}] Depois da ordenação: {local_data}")

gathered_data = None
if rank == 0:
    gathered_data = np.empty(N, dtype='i')

comm.Gather(local_data, gathered_data, root=0)

if rank == 0:
    bubble_sort(gathered_data)
    end_time = time.time()
    print("Vetor ordenado final:", gathered_data)
    print(f"Tempo total: {end_time - start_time:.6f} segundos")


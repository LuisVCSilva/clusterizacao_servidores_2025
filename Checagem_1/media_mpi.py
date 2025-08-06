from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    if rank == 0:
        print("Este programa requer pelo menos 2 processos.")
    MPI.Finalize()
    exit()

d0 = rank * 10 + 0
d1 = rank * 10 + 1
d2 = rank * 10 + 2
d3 = rank * 10 + 3

soma = d0 + d1 + d2 + d3

max_local = max(d0, d1, d2, d3)
media_local = soma / 4.0

medias = comm.gather(media_local, root=0)
maximos = comm.gather(max_local, root=0)

if rank == 0:
    print("Processo 0 recebeu os seguintes dados:")
    for i in range(size):
        print(f"Processo {i} -> média = {medias[i]:.2f}, máximo = {maximos[i]}")


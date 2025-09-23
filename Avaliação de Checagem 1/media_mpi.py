from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    if rank == 0:
        print("Execute com pelo menos 2 processos.")
else:
    if rank == 0:
        dado = 42
        print(f"Processo {rank} enviando dado: {dado} para processo 1")
        comm.send(dado, dest=1, tag=0)
    elif rank == 1:
        dado = comm.recv(source=0, tag=0)
        print(f"Processo {rank} recebeu dado: {dado} do processo 0")

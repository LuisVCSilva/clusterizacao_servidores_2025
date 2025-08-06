#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    int rank, size;
    int dado;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
    MPI_Comm_size(MPI_COMM_WORLD, &size); 

    if (size < 2) {
        if (rank == 0) {
            printf("Execute com pelo menos 2 processos.\n");
        }
        MPI_Finalize();
        return 0;
    }

    if (rank == 0) {
        dado = 42;
        printf("Processo %d enviando dado: %d para processo 1\n", rank, dado);
        MPI_Send(&dado, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    } else if (rank == 1) {
        MPI_Recv(&dado, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Processo %d recebeu dado: %d do processo 0\n", rank, dado);
    }

    MPI_Finalize(); 
    return 0;
}

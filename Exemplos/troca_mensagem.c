#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size, data;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank == 0) {
        data = 42;
        MPI_Send(&data, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
        printf("Processo 0 enviou %d para processo 1\n", data);
    } else if (rank == 1) {
        MPI_Recv(&data, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Processo 1 recebeu %d de processo 0\n", data);
    }

    MPI_Finalize();
    return 0;
}

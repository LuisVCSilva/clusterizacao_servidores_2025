#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size, i;
    float A[10];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank == 0) {
        for (i = 0; i < 10; i++) A[i] = i;
        for (int dest = 1; dest < size; dest++) {
            MPI_Send(A, 10, MPI_FLOAT, dest, 0, MPI_COMM_WORLD);
        }
    } else {
        MPI_Recv(A, 10, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }

    printf("Processo %d recebeu vetor:\n", rank);
    for (i = 0; i < 10; i++) printf("%.1f ", A[i]);
    printf("\n");

    MPI_Finalize();
    return 0;
}

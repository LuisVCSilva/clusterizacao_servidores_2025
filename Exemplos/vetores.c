#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size, i;
    float A[10];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    for (i = 0; i < 10; i++) {
        A[i] = i * rank;
    }

    printf("Processo %d:\n", rank);
    for (i = 0; i < 10; i++) {
        printf("%.1f ", A[i]);
    }
    printf("\n");

    MPI_Finalize();
    return 0;
}

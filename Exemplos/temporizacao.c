#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank;
    float data[100000];
    double t1, t2;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank == 0) {
        for (int i = 0; i < 100000; i++) data[i] = i;
        t1 = MPI_Wtime();
        MPI_Send(data, 100000, MPI_FLOAT, 1, 0, MPI_COMM_WORLD);
        t2 = MPI_Wtime();
        printf("Tempo de envio: %f segundos\n", t2 - t1);
    } else if (rank == 1) {
        MPI_Recv(data, 100000, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Processo 1 recebeu os dados\n");
    }

    MPI_Finalize();
    return 0;
}

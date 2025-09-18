#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define N 5
enum { THINKING, HUNGRY, EATING };

int estado;

int esquerda(int rank) { return (rank + N - 1) % N; }
int direita(int rank) { return (rank + 1) % N; }

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != N) {
        if (rank == 0) printf("Execute com exatamente %d processos.\n", N);
        MPI_Finalize();
        return 0;
    }

    srand(time(NULL) + rank);
    estado = THINKING;

    for (int step = 0; step < 10; step++) {

        printf("Filósofo %d pensando.\n", rank);
        sleep(rand() % 2);


        estado = HUNGRY;
        printf("Filósofo %d com fome.\n", rank);


        int estado_esq, estado_dir;
        MPI_Send(&estado, 1, MPI_INT, esquerda(rank), 0, MPI_COMM_WORLD);
        MPI_Send(&estado, 1, MPI_INT, direita(rank), 0, MPI_COMM_WORLD);


        MPI_Recv(&estado_esq, 1, MPI_INT, esquerda(rank), 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&estado_dir, 1, MPI_INT, direita(rank), 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        if (estado_esq != EATING && estado_dir != EATING) {
            estado = EATING;
            printf("Filósofo %d comendo.\n", rank);
            sleep(rand() % 2);
        } else {
            printf("Filósofo %d esperando.\n", rank);
        }

        estado = THINKING;
        MPI_Barrier(MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}


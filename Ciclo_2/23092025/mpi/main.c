// main.c
#include "meu_bcast.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank;
    int raiz = atoi(argv[1]); // raiz passada como argumento

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // --- TESTE COM MPI_Bcast ---
    char buffer[100];
    strcpy(buffer, "nada");
    if (rank == raiz) {
        strcpy(buffer, "olá!");
    }

    MPI_Bcast(buffer, sizeof(buffer), MPI_CHAR, raiz, MPI_COMM_WORLD);

    // --- TESTE COM MEU_Bcast ---
    char buffer2[100];
    strcpy(buffer2, "algo");
    if (rank == raiz) {
        strcpy(buffer2, "olá!");
    }

    MEU_Bcast(buffer2, sizeof(buffer2), MPI_CHAR, raiz, MPI_COMM_WORLD);

    // Comparando os resultados
    if (strcmp(buffer, buffer2) != 0) {
        printf("MPI_Bcast e MEU_Bcast deram resultados diferentes!\n");
    } else {
        printf("Rank %d recebeu: %s\n", rank, buffer2);
    }

    MPI_Finalize();
    return 0;
}

// bcast_tradicional.c
#include <mpi.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);

    int rank, tamanho;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &tamanho);

    int raiz = 0; // podemos fixar a raiz como 0
    char mensagem[100];

    if (rank == raiz) {
        strcpy(mensagem, "olá!");
        // Raiz envia para todos os outros
        for (int i = 0; i < tamanho; i++) {
            if (i != raiz) {
                MPI_Send(mensagem, sizeof(mensagem), MPI_CHAR, i, 0, MPI_COMM_WORLD);
                printf("Raiz enviou para Rank %d\n", i);
            }
        }
    } else {
        // Todos os outros recebem da raiz
        MPI_Recv(mensagem, sizeof(mensagem), MPI_CHAR, raiz, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Rank %d recebeu: %s\n", rank, mensagem);
    }

    MPI_Finalize();
    return 0;
}

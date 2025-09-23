#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define N 4  // tamanho fixo das matrizes

int main(int argc, char *argv[]) {
    int rank, size;
    int A[N][N], B[N][N], C[N][N];
    int A_line[N], C_line[N];
    int i, j, k;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != N) {
        if (rank == 0) {
            printf("Este programa requer exatamente %d processos.\n", N);
        }
        MPI_Finalize();
        return 0;
    }

    if (rank == 0) {

        printf("Matriz A:\n");
        for (i = 0; i < N; i++) {
            for (j = 0; j < N; j++) {
                A[i][j] = i + j;  
                printf("%3d ", A[i][j]);
            }
            printf("\n");
        }

        printf("Matriz B:\n");
        for (i = 0; i < N; i++) {
            for (j = 0; j < N; j++) {
                B[i][j] = (i == j) ? 1 : 0; 
                printf("%3d ", B[i][j]);
            }
            printf("\n");
        }

        // Distribui linhas de A
        for (i = 1; i < N; i++) {
            MPI_Send(A[i], N, MPI_INT, i, 0, MPI_COMM_WORLD);
        }


        for (j = 0; j < N; j++) {
            A_line[j] = A[0][j];
        }
    } else {

        MPI_Recv(A_line, N, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }

    MPI_Bcast(B, N * N, MPI_INT, 0, MPI_COMM_WORLD);

    for (j = 0; j < N; j++) {
        C_line[j] = 0;
        printf("Processo %d calculando C[%d][%d]: ", rank, rank, j);
        for (k = 0; k < N; k++) {
            int parcial = A_line[k] * B[k][j];
            C_line[j] += parcial;
            printf("%d*%d ", A_line[k], B[k][j]);
            if (k < N - 1) printf("+ ");
        }
        printf("= %d\n", C_line[j]);
    }

    printf("Processo %d chegou na BARREIRA.\n", rank);
    MPI_Barrier(MPI_COMM_WORLD);
    printf("Processo %d passou da BARREIRA.\n", rank);

    if (rank == 0) {
        // Recebe linhas de outros processos
        for (j = 0; j < N; j++) {
            C[0][j] = C_line[j];
        }

        for (i = 1; i < N; i++) {
            MPI_Recv(C[i], N, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        // Imprime resultado
        printf("\nMatriz C = A * B:\n");
        for (i = 0; i < N; i++) {
            for (j = 0; j < N; j++) {
                printf("%3d ", C[i][j]);
            }
            printf("\n");
        }
    } else {
        // Envia resultado da linha para processo 0
        MPI_Send(C_line, N, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}

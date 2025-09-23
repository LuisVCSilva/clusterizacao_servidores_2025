// meu_bcast.c
#include "meu_bcast.h"
#include <mpi.h>
#include <stdio.h>

/*
 * Broadcast em árvore binária com prints detalhados
 */
int MEU_Bcast(void *buffer, int contagem, MPI_Datatype tipo, int raiz, MPI_Comm comunicador) {
    int rank, tamanho;
    MPI_Comm_rank(comunicador, &rank); // rank do processo
    MPI_Comm_size(comunicador, &tamanho); // total de processos

    int rank_relativo = (rank + tamanho - raiz) % tamanho; // rank relativo à raiz
    int mascara = 1;

    // --- FASE DE RECEBIMENTO ---
    while (mascara < tamanho) {
        if (rank_relativo & mascara) { // se tiver bit ligado
            int pai = rank_relativo & (~mascara); // calcula o pai na árvore
            pai = (pai + raiz) % tamanho; // ajusta para rank real
            MPI_Recv(buffer, contagem, tipo, pai, 0, comunicador, MPI_STATUS_IGNORE);
            printf("Rank %d recebeu a mensagem do Rank %d\n", rank, pai);
            break;
        }
        mascara <<= 1;
    }

    // --- FASE DE ENVIO ---
    mascara >>= 1;
    while (mascara > 0) {
        if ((rank_relativo + mascara) < tamanho) { // verifica se existe filho
            int filho = rank_relativo + mascara;
            filho = (filho + raiz) % tamanho; // ajusta para rank real
            MPI_Send(buffer, contagem, tipo, filho, 0, comunicador);
            printf("Rank %d enviou a mensagem para Rank %d\n", rank, filho);
        }
        mascara >>= 1;
    }

    return MPI_SUCCESS;
}


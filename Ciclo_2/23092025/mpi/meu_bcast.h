// meu_bcast.h
#ifndef MEU_BCAST_H
#define MEU_BCAST_H

#include <mpi.h>

// Protótipo da função de broadcast em árvore binária
int MEU_Bcast(void *buffer, int contagem, MPI_Datatype tipo, int raiz, MPI_Comm comunicador);

#endif

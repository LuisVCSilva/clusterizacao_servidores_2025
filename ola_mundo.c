#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size;

    MPI_Init(&argc, &argv); // Inicializa MPI
    MPI_Comm_size(MPI_COMM_WORLD, &size); // Número total de processos
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // ID do processo atual

    printf("Olá do processo %d de %d\n", rank, size);

    MPI_Finalize(); // Finaliza MPI
    return 0;
}
/* Relato de Caio
 * Esse programa é escrito em c, e utiliza a biblioteca de mpi para
 * aplicar o conceito de clusterização utilizando os núcleos do processador
 * no lugar de computadores e máquinas virtuais. O código executa a mesma tarefa
 * que nesse caso é um printf em vários núcleos simultaneamente.
 * O conceito de clusterização tem como objetivo dividir tarefas em diferentes máquinas
 * agilizando o processo e o código aplica isso com os núcleos.*/

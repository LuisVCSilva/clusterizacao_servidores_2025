#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

// Função Bubble Sort simples
void bubble_sort(int *array, int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (array[j] > array[j+1]) {
                int tmp = array[j];
                array[j] = array[j+1];
                array[j+1] = tmp;
            }
        }
    }
}

int main(int argc, char** argv) {
    int rank, size, n = 16; 
    int *data = NULL;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int local_n = n / size;
    int *local_data = (int*)malloc(local_n * sizeof(int));


    if (rank == 0) {
        data = (int*)malloc(n * sizeof(int));
        printf("Vetor original:\n");
        for (int i = 0; i < n; i++) {
            data[i] = rand() % 100;
            printf("%d ", data[i]);
        }
        printf("\n");
    }


    MPI_Scatter(data, local_n, MPI_INT, local_data, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    bubble_sort(local_data, local_n);

    MPI_Gather(local_data, local_n, MPI_INT, data, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        bubble_sort(data, n);

        printf("Vetor ordenado final:\n");
        for (int i = 0; i < n; i++) {
            printf("%d ", data[i]);
        }
        printf("\n");

        free(data);
    }

    free(local_data);
    MPI_Finalize();
    return 0;
}


================
Compile e execute o código Bubble Sort com MPI fornecido.
2 Modifique o vetor para os tamanhos: 32, 64, 128 e 256 elementos.
3 Execute com 2, 4 e 8 processos, e registre o tempo de execução.
4 Faça cada processo imprimir seu vetor local antes e depois da
ordenação.
5 (Opcional) Implemente uma fusão (merge) no processo 0 para
substituir a ordenação final.
6 Responda:
Qual o impacto do número de processos no tempo?
Em quais situações houve ganho real?
Quais limitações você identificou?
Como melhorar a eficiência do algoritmo?





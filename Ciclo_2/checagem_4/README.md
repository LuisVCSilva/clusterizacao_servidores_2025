# Checagem 4 -- MPI Dining Philosophers

Nessa checagem vocês trabalharão com o clássico problema do Jantar dos Filósofos (visto em seminários) utilizando MPI (Message Passing Interface). O objetivo é explorar conceitos de sincronização, exclusão mútua e comunicação entre processos, identificando problemas de concorrência e deadlock.

Cada filósofo é modelado como um processo MPI que alterna entre pensar e comer, competindo por recursos compartilhados (os garfos).

## Atividade prática

### O que os alunos devem fazer:

1. Compilar e executar o código base em MPI com 5 processos.

   * Atenção: o código fornecido contém um bug proposital que pode causar deadlock eventualmente.

2. Analisar o código e identificar o bug.

   * Comente qual é o problema, por que ele leva a deadlock e em que situação ocorre.

3. Corrigir o bug no código.

   * Garanta que a comunicação entre processos não trave o programa.
   * Explique a correção implementada.

4. Com a versão corrigida, observar o comportamento de sincronização (bônus):

   * Tempos de espera para comer;
   * Possíveis bloqueios ou contenção pelos garfos.

5. Produzir um relatório discutindo:

   * Tempos de espera e possíveis bloqueios ou contenção pelos garfos;
   * O bug inicial e como ele foi corrigido.

---

### Critérios de avaliação

* Identificação correta do bug de deadlock no código fornecido.
* Implementação funcional da comunicação via MPI (sem travamentos).
* Criação e utilização correta de clusters com `MPI_Comm_split`.
* Organização, comentários e clareza no código entregue.

---

### Sugestão de modificação no código

* Alterar a função de comunicação entre filósofos para evitar deadlock (ex.: substituir `MPI_Send` por `...`).
* Implementar métricas de tempo de espera de cada filósofo até conseguir comer.
* Agrupar filósofos em clusters e coordenar recursos apenas dentro de cada cluster.
* Documentar claramente o problema identificado e a solução adotada.

---

### Possíveis Entregáveis

1. Documentação / README:

   * Explicação de como compilar e executar o código.
   * Descrição do bug encontrado e da correção implementada.

2. Código fonte:

   * Versão base do jantar dos filósofos com bug.
   * Versão corrigida com comunicação segura.

3. Relatório:

   * Tempos médios de espera de cada filósofo.
   * Casos de bloqueio ou deadlock observados.

4. Evidências / prints:

   * Execução do programa mostrando filósofos pensando, comendo e esperando.
   * Prints de análises comparativas e métricas de espera.

---

Entrega: via email para `luisvinicius.professor@uniatenas.edu.br` ou commit no repositório forkado.


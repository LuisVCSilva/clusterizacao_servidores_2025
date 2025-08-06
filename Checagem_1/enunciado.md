
# Avaliação de Checagem — MPI em Laboratório
## Aplicações de clusterização em servidores

**Tema:** Comunicação entre processos com MPI (Scatter, Gather, rank, size)  
**Aluno:** Caio Corrêa de Castro 
**Data:** 05/05/2025

---

###  Objetivo

Executar, analisar e modificar um programa MPI que distribui dados entre processos, realiza cálculos locais e coleta os resultados para ordenação.

---

###  Arquivo base

O código que você deve utilizar está nesse diretorio:

```
media_mpi.c
```

Compile com:

```bash
mpicc media_mpi.c -o media_mpi
```

Execute com:

```bash
mpirun -np 4 ./media_mpi
```

---

### Parte 1 — Execução básica

#### 1.1. Saída esperada

Execute o programa com 4 processos. Copie aqui a saída do terminal:

```
Processo 0 enviando dado: 42 para processo 1
Processo 1 recebeu dado: 42 do processo 0
```

---

###  Parte 2 — Análise de funcionamento

#### 2.1. O que faz `MPI_Scatter` neste código?

_Resposta:_ O MPI_Scatter tem como objetivo distribuir entre os processo, mas não está no código.

--- 

#### 2.2. Qual o papel de `MPI_Gather`?

_Resposta:_ O MPI_ Gather irá recolher todos processos que foram divididos e juntá-los, mas também não está no código.

---

#### 2.3. Por que a ordenação das médias acontece apenas no processo 0?

_Resposta:_ Porque ele está como processo 

---

###  Parte 3 — Modificação

#### 3.1. Modifique o código para que **cada processo envie também seu maior valor local**, além da média.

Use `MPI_Gather` para coletar ambos os dados no processo 0.

 - Faça um **commit com sua modificação** e anexe abaixo o arquivo completo.

---

### 3.2. Copie aqui a saída do seu programa modificado:

```
Processo 0 recebeu os seguintes dados:
Processo 0 -> média = 1.50, máximo = 3
Processo 1 -> média = 11.50, máximo = 13
Processo 2 -> média = 21.50, máximo = 23
Processo 3 -> média = 31.50, máximo = 33

```

---

### Análise com utilitários Linux

#### 4.1. Use o comando `time` para medir o tempo de execução do programa com 2, 4 e 6 processos.

Anote abaixo:

| Processos | Tempo (real) |
|-----------|--------------|
| 2         |     333.67 ms|
| 4         |     350.44 ms|
| 6         |     359.83 ms|

#### 4.2. Use `htop` ou `top` para observar o uso de CPU. O uso foi balanceado entre os processos?

_Resposta:_ Sim os o uso da cpu foi balanceada entre os processos.

---

#### 4.3. Use `strace`, `taskset` ou `MPI_Wtime` para investigar comportamento adicional do programa. Comente algo que tenha achado interessante:

_Resposta:_

---

### Observações

- Faça commits frequentes com mensagens claras.
- Crie um `commit` final com a tag `atividade-finalizada`.
- Envie o link do seu repositório *forkado* com a atividade completa para luis.professor@uniatenas.edu.br

---

**Boa prática!**

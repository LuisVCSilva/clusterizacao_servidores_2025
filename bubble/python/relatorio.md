# 📊 Análise do Bubble Sort com MPI

## ✅ Experimentos Realizados

- **Tamanhos de vetor testados:** `32`, `64`, `128`, `256`
- **Processos utilizados:** `2`, `4`, `8`
- Cada processo imprime seu vetor local **antes e depois** da ordenação local.
- A ordenação final foi feita no processo 0 com Bubble Sort (sequencial).

---

## ❓ Qual o impacto do número de processos no tempo?

- Com o aumento do número de processos, o tempo de **ordenação local** tende a diminuir, pois cada processo recebe menos elementos.
- No entanto, há uma **sobrecarga de comunicação** com `MPI_Scatter` e `MPI_Gather`.
- A ordenação final no processo 0 ainda é **sequencial**, o que limita o ganho total de desempenho.

---

## 💡 Em quais situações houve ganho real?

- Ganhos mais evidentes ocorreram com vetores de tamanho `128` e `256` usando `4` ou `8` processos.
- Para vetores muito pequenos (`32`, `64`), o tempo de comunicação superou os benefícios do paralelismo.

---

## ⚠️ Quais limitações você identificou?

- **Bubble Sort** é um algoritmo ineficiente para ordenação, com complexidade `O(n²)`.
- A etapa final de ordenação no processo 0 **não é paralela**, tornando-se um gargalo.
- Se `N` não for divisível por `size`, é necessário usar `MPI_Scatterv` para evitar perda de dados ou desequilíbrio.
- O ganho de desempenho **não é linear** com o aumento do número de processos.

---

## 🚀 Como melhorar a eficiência do algoritmo?

1. **Substituir o Bubble Sort** por algoritmos mais eficientes:
   - `Merge Sort`
   - `Quick Sort`

2. **Implementar fusão paralela** (ex: merge em árvore binária ou hypercube) em vez de `MPI_Gather` seguido de ordenação.

3. Utilizar **`MPI_Scatterv` e `MPI_Gatherv`** para suportar tamanhos de vetor não divisíveis igualmente pelo número de processos.

4. Adicionar **temporalização de cada fase** para análise detalhada dos gargalos:
   - Tempo de comunicação
   - Tempo de ordenação local
   - Tempo de fusão final

---

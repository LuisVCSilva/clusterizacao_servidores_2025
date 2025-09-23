mpicc main.c meu_bcast.c -o meu_bcast
mpicc bcast_tradicional.c -o bcast_tradicional

time mpirun -np 8 ./meu_bcast 0
0,38s user 0,34s system 127% cpu 0,558 total

time mpirun -np 8 ./bcast_tradicional
0,39s user 0,34s system 120% cpu 0,603 total


====
Com 8 processos em máquina local, os tempos são muito próximos:

MEU_Bcast: 0,558 s
Tradicional: 0,603 s

Diferença pequena devido a poucos processos


====

mpirun -np 64 --oversubscribe ./meu_bcast 0  40,39s user 6,43s system 1087% cpu 4,306 total
mpirun -np 64 --oversubscribe ./bcast_tradicional 0  40,13s user 6,39s system 1090% cpu 4,265 total



mpirun -np 128 --oversubscribe ./meu_bcast 0  175,14s user 16,64s system 1378% cpu 13,914 total
mpirun -np 128 --oversubscribe ./bcast_tradicional  159,56s user 14,74s system 1393% cpu 12,512 total

mpirun -np 256 --oversubscribe ./bcast_tradicional  732,32s user 61,49s system 1517% cpu 52,309 total
mpirun -np 256 --oversubscribe ./meu_bcast 0  706,29s user 54,27s system 1516% cpu 50,141 total

Conclusão:
- Para baixo número de processos (64), a diferença entre os algoritmos é mínima.
- Com aumento de processos (128 e 256), o broadcast em árvore binária (`meu_bcast`) apresenta melhor escalabilidade, com tempos totais ligeiramente menores que o broadcast tradicional.
- Isso evidencia que a otimização em árvore binária reduz o tempo de disseminação da mensagem em clusters maiores.

No broadcast tradicional simples, um processo (a raiz) envia a mensagem para todos os outros processos de forma sequencial. Se houver p processos, o tempo de comunicação cresce proporcionalmente a O(p). 
Na prática, isso significa que, à medida que aumentamos o número de processos, o tempo total aumenta de maneira praticamente linear. Observando os resultados obtidos nos testes, percebe-se esse crescimento: para 64 processos, o tempo total foi de aproximadamente 4,265 segundos; para 128 processos, subiu para 12,512 segundos; e para 256 processos, chegou a 52,309 segundos, evidenciando o impacto do aumento do número de processos na performance do broadcast tradicional.
No broadcast em árvore binária, a mensagem é propagada seguindo uma estrutura de árvore, onde cada processo envia a mensagem para dois filhos, que por sua vez repassam para os seus filhos, e assim por diante. Isso reduz o número de passos de comunicação para O(log p). Em um cluster com muitos nós, esse esquema escala muito melhor que o broadcast tradicional, diminuindo congestionamento da rede e acelerando a disseminação da mensagem, mesmo quando o número de processos é grande.

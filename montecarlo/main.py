from mpi4py import MPI
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

total_pontos = 100000
pontos_por_processo = total_pontos // size

# Gera pontos aleatórios usando NumPy
x = np.random.rand(pontos_por_processo)
y = np.random.rand(pontos_por_processo)

# Calcula quais pontos estão dentro do círculo
dist_sq = x**2 + y**2
dentro = dist_sq <= 1

acertos_local = np.sum(dentro)

print(f"Processo {rank}: gerou {pontos_por_processo} pontos, {acertos_local} dentro do círculo")

# Reduz para obter soma total
acertos_total = comm.reduce(acertos_local, op=MPI.SUM, root=0)

# Apenas o processo 0 calcula e exibe resultado final e gráfico
if rank == 0:
    pi_estimado = 4 * acertos_total / total_pontos
    print(f"Estimativa de pi: {pi_estimado}")

    # Junta pontos de todos os processos para plotar
    todos_x = comm.gather(x, root=0)
    todos_y = comm.gather(y, root=0)
    todos_dentro = comm.gather(dentro, root=0)

    X = np.concatenate(todos_x)
    Y = np.concatenate(todos_y)
    Dentro = np.concatenate(todos_dentro)

    sns.scatterplot(x=X[~Dentro], y=Y[~Dentro], color="red", s=10, label="Fora do círculo")
    sns.scatterplot(x=X[Dentro], y=Y[Dentro], color="blue", s=10, label="Dentro do círculo")

    circle = plt.Circle((0, 0), 1, color='black', fill=False)
    plt.gca().add_artist(circle)

    plt.axis("equal")
    plt.legend()
    plt.title(f"Monte Carlo - Estimativa de π: {pi_estimado}")
    plt.show()
else:
    comm.gather(x, root=0)
    comm.gather(y, root=0)
    comm.gather(dentro, root=0)

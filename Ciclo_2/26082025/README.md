# NF2 – Aplicação de Clusterização em Servidores Virtuais

--------------------------------------------------------
1. Preparando o Ambiente

1. Limpar redes antigas do Mininet
sudo mn -c

2. Verificar distribuição WSL
wsl --list --verbose
Se a coluna VERSION for 1, migre para WSL 2:
wsl --set-version Ubuntu 2

3. Atualizar pacotes no Ubuntu
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential python3 git net-tools iproute2 mininet

--------------------------------------------------------
2. Criando e Explorando a Topologia

2.1 Topologia Star mínima
- 1 switch (s1) e 2 hosts (h1, h2).
- Conecta todos os hosts a um único switch central.
sudo mn --topo single,2 --mac --switch=userspace

2.2 Comandos básicos do Mininet
mininet> nodes        # lista hosts e switches
mininet> net          # mostra links e interfaces
mininet> h1 ifconfig  # IP e interfaces do host h1
mininet> h2 ifconfig
mininet> h1 ping h2   # teste de conectividade
mininet> link h1 s1 down # simula falha de link
mininet> link h1 s1 up   # restaura link
mininet> exit

--------------------------------------------------------
3. Rodando Experimentos com Scripts

3.1 Script star.py
Automatiza:
- Criação da topologia Star com h1, h2 e s1
- Testes de conectividade (ping)
- Coleta de estatísticas de CPU
- Medição de latência
- Plotagem de gráficos
- Execução de MPI

Execução:
sudo python3 star.py

3.2 Script mpi_experiment.py
- Executa computação distribuída usando MPI
- Deve ser rodado em cada host

Execução manual:
h1 mpirun --allow-run-as-root -np 1 python3 mpi_experiment.py
h2 mpirun --allow-run-as-root -np 1 python3 mpi_experiment.py

Como root local:
OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
mpirun -np 1 python3 mpi_experiment.py

--------------------------------------------------------
4. Observando Resultados

- Ping entre hosts sem perdas (0% dropped)
- Gráficos de CPU e latência
- Resultados MPI: tempo de execução por rank

Use os gráficos para interpretar: qual host teve maior carga? Há equilíbrio de tarefas?

--------------------------------------------------------
5. Exercícios Rápidos

1. Liste hosts e switches com nodes.
2. Teste IPs e conectividade (ifconfig, ping).
3. Rode star.py e analise gráficos de CPU.
4. Rode mpi_experiment.py em h1 e h2; registre tempo de execução.
5. Simule falha de link (link h1 s1 down) e compare latência.
6. Expanda a topologia para 4 hosts; observe alteração de desempenho.
7. Responda:
   - Como a topologia em estrela influencia a comunicação?
   - Vantagens e limitações da topologia Star?
   - Qual host foi mais eficiente na execução MPI?

Todas as respostas devem ser registradas em respostas.md e commitadas no seu fork.

--------------------------------------------------------
6. Dicas finais

- Garanta que os scripts estejam no mesmo diretório do repositório.
- Mininet e OpenMPI devem estar instalados.
- CLI do Mininet permite testes adicionais e aprendizado interativo.


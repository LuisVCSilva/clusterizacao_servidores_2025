#!/usr/bin/python3
"""
star.py - Experimentos de cluster, MPI e rede no Mininet
Topologia: single switch com 2 hosts
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import matplotlib.pyplot as plt
import random
import time
import os

def cluster_topology():
    net = Mininet(link=TCLink, switch=OVSSwitch)

    # Criar switch e hosts
    s1 = net.addSwitch('s1', failMode='standalone')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    # Criar links
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    # Iniciar rede
    net.start()

    print("*** Testando conectividade")
    net.pingAll()

    return net, h1, h2

def run_cpu_test(host, duration=5):#pra fazer
    """Simula carga de CPU no host e coleta estatísticas"""
    stats = []
    for i in range(duration):
        #cpu_usage = random.randint(20, 80)
        stats.append(cpu_usage)
        time.sleep(1)
    return stats

def run_network_test(h1, h2, duration=5):
    """Testa latência entre hosts"""
    stats = []
    for i in range(duration):
        result = h1.cmd(f'ping -c 1 {h2.IP()}')
        try:
            latency = float(result.split('time=')[1].split(' ')[0])
        except:
            latency = None
        stats.append(latency)
        time.sleep(1)
    return stats

def plot_stats(cpu_h1, cpu_h2, latency):
    plt.figure(figsize=(10,5))
    plt.subplot(2,1,1)
    plt.plot(cpu_h1, label='CPU h1')
    plt.plot(cpu_h2, label='CPU h2')
    plt.ylabel('Uso de CPU (%)')
    plt.title('Estatísticas de CPU dos hosts')
    plt.legend()

    plt.subplot(2,1,2)
    plt.plot(latency, label='Latência h1->h2')
    plt.ylabel('Tempo (ms)')
    plt.xlabel('Segundos')
    plt.title('Latência de rede')
    plt.legend()

    plt.tight_layout()
    plt.show()

def run_mpi_test(host):
    """Executa o experimento MPI dentro do host"""#talvez bug no wsl
    cmd = (
        "env OMPI_ALLOW_RUN_AS_ROOT=1 "
        "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 "
        "mpirun -np 1 python3 mpi_experiment.py &"
    )
    host.cmd(cmd)

if __name__ == '__main__':
    setLogLevel('info')

    # Limpar redes antigas
    os.system("sudo mn -c")

    # Criar topologia
    net, h1, h2 = cluster_topology()

    print("*** Rodando teste de CPU")
    cpu_h1 = run_cpu_test(h1)
    cpu_h2 = run_cpu_test(h2)

    print("*** Rodando teste de rede")
    latency = run_network_test(h1, h2)

    print("*** Plotando resultados")
    plot_stats(cpu_h1, cpu_h2, latency)

    print("*** Executando MPI em cada host")
    run_mpi_test(h1)
    run_mpi_test(h2)

    print("*** CLI do Mininet aberta. Você pode rodar comandos adicionais ou observar hosts.")
    CLI(net)

    net.stop()

#!/usr/bin/python3
"""
complex_cluster.py - Experimento de cluster distribuído com falhas e ruído
Topologia: 2 switches e 4 hosts
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

def complex_topology():
    net = Mininet(link=TCLink, switch=OVSSwitch)

    # Criar switches e hosts
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')

    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')

    # Conectar hosts aos switches
    net.addLink(h1, s1, bw=10, delay='5ms')
    net.addLink(h2, s1, bw=10, delay='5ms')
    net.addLink(h3, s2, bw=10, delay='5ms')
    net.addLink(h4, s2, bw=10, delay='5ms')

    # Conectar switches entre si
    net.addLink(s1, s2, bw=20, delay='10ms')

    net.start()
    print("*** Testando conectividade inicial")
    net.pingAll()

    return net, [h1,h2,h3,h4]

def run_cpu_test(hosts, duration=5):
    """Simula carga de CPU variada"""
    cpu_stats = {h.name: [] for h in hosts}
    for _ in range(duration):
        for h in hosts:
            usage = random.randint(20, 90)  # Simula ruído de CPU
            cpu_stats[h.name].append(usage)
        time.sleep(1)
    return cpu_stats

def run_network_test(hosts, duration=5):
    """Simula ruído de rede e falhas intermitentes"""
    latency_stats = {f"{h1.name}->{h2.name}": [] 
                     for i,h1 in enumerate(hosts) for j,h2 in enumerate(hosts) if i<j}
    
    for _ in range(duration):
        for i,h1 in enumerate(hosts):
            for j,h2 in enumerate(hosts):
                if i<j:
                    # Simular falha aleatória
                    if random.random() < 0.1:  # 10% pacotes perdidos
                        latency = None
                    else:
                        latency = random.uniform(1, 20)  # ms
                    latency_stats[f"{h1.name}->{h2.name}"].append(latency)
        time.sleep(1)
    return latency_stats

def plot_stats(cpu_stats, latency_stats):
    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    for h, stats in cpu_stats.items():
        plt.plot(stats, label=f'CPU {h}')
    plt.ylabel('Uso de CPU (%)')
    plt.title('CPU Hosts')
    plt.legend()

    plt.subplot(2,1,2)
    for pair, stats in latency_stats.items():
        plt.plot([s if s is not None else 0 for s in stats], label=pair)
    plt.ylabel('Latência (ms)')
    plt.xlabel('Segundos')
    plt.title('Latência de Rede (com falhas simuladas)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def run_mpi_test(hosts):
    """Executa experimento distribuído MPI real"""
    for h in hosts:
        cmd = (
            "env OMPI_ALLOW_RUN_AS_ROOT=1 "
            "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 "
            "mpirun -np 1 python3 mpi_real_problem.py &"
        )
        h.cmd(cmd)

if __name__ == '__main__':
    setLogLevel('info')
    os.system("sudo mn -c")

    net, hosts = complex_topology()
    cpu_stats = run_cpu_test(hosts)
    latency_stats = run_network_test(hosts)

    plot_stats(cpu_stats, latency_stats)
    run_mpi_test(hosts)

    CLI(net)
    net.stop()

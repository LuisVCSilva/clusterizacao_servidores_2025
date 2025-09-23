#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import matplotlib.pyplot as plt
import numpy as np
import random

def create_topology():
    net = Mininet(switch=OVSSwitch, link=TCLink)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Criar hosts
    hosts = [net.addHost(f'h{i+1}') for i in range(4)]

    # Criar switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Conectar hosts a switches
    net.addLink(hosts[0], s1)
    net.addLink(hosts[1], s1)
    net.addLink(hosts[2], s2)
    net.addLink(hosts[3], s2)

    # Conectar switches com ruído
    def noisy_link(switch1, switch2):
        delay = f"{random.randint(10,30)}ms"
        loss = random.uniform(1,5)
        net.addLink(switch1, switch2, bw=10, delay=delay, loss=loss)

    noisy_link(s1, s2)

    return net, hosts

def measure_latencies(hosts):
    n = len(hosts)
    latencies = np.zeros((n, n))

    for i, h1 in enumerate(hosts):
        for j, h2 in enumerate(hosts):
            if i == j:
                latencies[i, j] = 0.0
                continue
            # ping rápido (1 pacote)
            result = h1.cmd(f'ping -c 1 {h2.IP()}')
            try:
                line = [l for l in result.splitlines() if 'rtt min/avg/max' in l][0]
                avg_rtt = float(line.split('/')[4])
                latencies[i, j] = avg_rtt
            except:
                latencies[i, j] = np.nan

    return latencies

def plot_heatmap(latencies, hosts):
    plt.figure(figsize=(6,5))
    plt.imshow(latencies, cmap='hot', interpolation='nearest')
    plt.colorbar(label='RTT médio (ms)')
    plt.xticks(range(len(hosts)), [h.name for h in hosts])
    plt.yticks(range(len(hosts)), [h.name for h in hosts])
    plt.title('Heatmap de latência entre hosts')
    plt.tight_layout()
    plt.show()

def plot_boxplot(latencies, hosts):
    plt.figure(figsize=(6,4))
    plt.boxplot([latencies[i,:][latencies[i,:]>0] for i in range(len(hosts))],
                labels=[h.name for h in hosts])
    plt.ylabel('Latência (ms)')
    plt.title('Boxplot de latência por host')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    setLogLevel('info')
    net, hosts = create_topology()
    net.start()

    info("*** Testando conectividade básica\n")
    net.pingAll()

    info("*** Medindo latências entre hosts\n")
    latencies = measure_latencies(hosts)

    info("*** Plotando heatmap\n")
    plot_heatmap(latencies, hosts)

    info("*** Plotando boxplot\n")
    plot_boxplot(latencies, hosts)

    CLI(net)
    net.stop()


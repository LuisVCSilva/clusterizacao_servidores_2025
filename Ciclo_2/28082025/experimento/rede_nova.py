#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import matplotlib.pyplot as plt

def get_latency(src, dst):
    """Retorna RTT em ms ou None se falhar"""
    result = src.cmd(f'ping -c1 -W1 {dst.IP()}')  # -W1 timeout 1s
    if 'time=' in result:
        try:
            return float(result.split('time=')[1].split(' ms')[0])
        except:
            return None
    else:
        return None

def run_extended_topology():
    net = Mininet(switch=OVSSwitch, link=TCLink)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Hosts originais
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')

    # Switches originais
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Links originais com ruído
    net.addLink(h1, s1, bw=10, delay='20ms', loss=2)
    net.addLink(h2, s1, bw=10, delay='20ms', loss=2)
    net.addLink(h3, s2, bw=10, delay='25ms', loss=3)
    net.addLink(h4, s2, bw=10, delay='25ms', loss=3)
    net.addLink(s1, s2, bw=10, delay='30ms', loss=1)

    # Novo cluster
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    s3 = net.addSwitch('s3')
    net.addLink(h5, s3, bw=10, delay='15ms', loss=2)
    net.addLink(h6, s3, bw=10, delay='15ms', loss=2)
    net.addLink(s2, s3, bw=10, delay='20ms', loss=1)  # conecta ao cluster existente

    net.start()
    info("*** Testando conectividade\n")
    #net.pingAll()

    # Medição simples de latência
    hosts = [h1, h2, h3, h4, h5, h6]
    lat_matrix = []
    for src in hosts:
        row = []
        for dst in hosts:
            if src == dst:
                row.append(0)
            else:
                latency = get_latency(src, dst)
                row.append(latency if latency is not None else float('nan'))
        lat_matrix.append(row)

    # Heatmap
    plt.imshow(lat_matrix, cmap='YlOrRd', interpolation='nearest')
    plt.colorbar(label='Latência (ms)')
    plt.xticks(range(len(hosts)), [h.name for h in hosts])
    plt.yticks(range(len(hosts)), [h.name for h in hosts])
    plt.title('Heatmap de latência entre hosts')
    plt.show()

    # Boxplot
    plt.boxplot(lat_matrix)
    plt.xticks(range(1, len(hosts)+1), [h.name for h in hosts])
    plt.ylabel('Latência (ms)')
    plt.title('Boxplot de latência por host')
    plt.show()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_extended_topology()

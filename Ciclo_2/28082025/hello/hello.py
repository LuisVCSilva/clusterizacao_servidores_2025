#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def run_distributed_computation():
    net = Mininet(switch=OVSSwitch)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    s1 = net.addSwitch('s1')
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.start()
    info("*** Testando conectividade\n")
    net.pingAll()

    info("*** Criando e rodando scripts nos hosts\n")

    # Script h1 (servidor)
    h1_script = (
        "import socket\n"
        "logfile='/tmp/h1_log'\n"
        "with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n"
        "    s.bind(('',5000))\n"
        "    s.listen()\n"
        "    conn, addr = s.accept()\n"
        "    with conn, open(logfile,'w') as f:\n"
        "        f.write('Host h1 rodando\\n')\n"
        "        f.write('Enviando numero 42\\n')\n"
        "        conn.sendall(b'42')\n"
        "        result = conn.recv(1024)\n"
        "        f.write('Resultado recebido de h2: {}\\n'.format(result.decode()))\n"
    )

    # Script h2 (cliente)
    h2_script = (
        "import socket, time\n"
        "logfile='/tmp/h2_log'\n"
        "time.sleep(1)\n"
        "with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n"
        "    s.connect(('10.0.0.1',5000))\n"
        "    with open(logfile,'w') as f:\n"
        "        f.write('Host h2 rodando\\n')\n"
        "        data = s.recv(1024)\n"
        "        f.write('Numero recebido de h1: {}\\n'.format(data.decode()))\n"
        "        processed = int(data.decode())*2\n"
        "        f.write('Numero processado: {}\\n'.format(processed))\n"
        "        s.sendall(str(processed).encode())\n"
    )

    # Executa scripts nos hosts
    h1.popen(['python3', '-c', h1_script])
    h2.popen(['python3', '-c', h2_script])

    info("*** Comunicação iniciada. Verifique logs:\n")
    info("mininet> h1 cat /tmp/h1_log\n")
    info("mininet> h2 cat /tmp/h2_log\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_distributed_computation()


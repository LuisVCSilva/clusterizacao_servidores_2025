import os
import socket
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------
# Função de simulação Monte Carlo
# ---------------------------
def monte_carlo_pi(num_samples: int) -> float:
    inside_circle = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            inside_circle += 1
    return (4.0 * inside_circle) / num_samples


# ---------------------------
# Endpoints
# ---------------------------

@app.route('/')
def index():
    return jsonify({
        "message": "Olá do app Flask + Kubernetes!",
        "endpoints": [
            "/docker-info",
            "/montecarlo/<n>",
            "/montecarlo-distributed/<n>"
        ]
    })


@app.route('/docker-info')
def docker_info():
    """Retorna informações do container Docker atual"""
    info = {
        "hostname": socket.gethostname(),
        "cwd": os.getcwd(),
        "env": dict(list(os.environ.items())[:10])  # só os 10 primeiros envs
    }
    return jsonify(info)


@app.route('/montecarlo/<int:n>')
def montecarlo_single(n):
    """Monte Carlo single CPU (local, dentro de 1 container)"""
    pi_estimate = monte_carlo_pi(n)
    return jsonify({
        "samples": n,
        "pi_estimate": pi_estimate,
        "mode": "single-cpu"
    })


@app.route('/montecarlo-distributed/<int:n>')
def montecarlo_distributed(n):
    """
    Monte Carlo distribuído: divide o total de amostras (n)
    entre todos os pods (réplicas) do deployment.
    
    Estratégia: 
      - usa env var POD_REPLICAS para saber número de réplicas
      - usa env var POD_INDEX para simular ID do pod
      - cada pod executa sua parte
    """
    replicas = int(os.getenv("POD_REPLICAS", "1"))
    pod_index = int(os.getenv("POD_INDEX", "0"))

    # dividir amostras
    per_pod = n // replicas
    pi_estimate = monte_carlo_pi(per_pod)

    return jsonify({
        "samples_total": n,
        "samples_this_pod": per_pod,
        "replicas": replicas,
        "pod_index": pod_index,
        "pi_partial": pi_estimate,
        "note": "Resultados devem ser agregados fora (ex: via Service + client aggregator)."
    })


# ---------------------------
# Run
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


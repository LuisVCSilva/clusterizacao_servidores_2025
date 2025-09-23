import requests
import os

# URL base do Service
SERVICE_HOST = os.getenv("SERVICE_HOST", "127.0.0.1")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8080")

# Número total de amostras
TOTAL_SAMPLES = 1000000

# Número de réplicas (pods)
REPLICAS = int(os.getenv("POD_REPLICAS", "3"))

def aggregate_montecarlo(total_samples, replicas):
    pi_sum = 0.0
    samples_per_pod = total_samples // replicas

    for pod_index in range(replicas):
        # Chamando o endpoint de cada pod via Service
        url = f"http://{SERVICE_HOST}:{SERVICE_PORT}/montecarlo-distributed/{total_samples}"
        try:
            response = requests.get(url)
            data = response.json()
            pi_partial = data.get("pi_partial", 0)
            pi_sum += pi_partial
            print(f"Pod {pod_index}: partial pi = {pi_partial}")
        except Exception as e:
            print(f"Erro ao chamar pod {pod_index}: {e}")

    # Média das estimativas parciais
    pi_aggregate = pi_sum / replicas
    return pi_aggregate

if __name__ == "__main__":
    pi_estimate = aggregate_montecarlo(TOTAL_SAMPLES, REPLICAS)
    print(f"Estimated PI (aggregated) = {pi_estimate}")

import pytest
from app import app, monte_carlo_pi

# ------------------------
# Fixture para criar test client
# ------------------------
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# ------------------------
# Teste do endpoint /change
# ------------------------
def test_change_endpoint(client):
    # Chamando endpoint antigo /montecarlo/10000
    response = client.get("/montecarlo/10000")
    assert response.status_code == 200
    data = response.get_json()
    assert "pi_estimate" in data
    assert data["mode"] == "single-cpu"
    assert data["samples"] == 10000

# ------------------------
# Teste do endpoint /docker-info
# ------------------------
def test_docker_info(client):
    response = client.get("/docker-info")
    assert response.status_code == 200
    data = response.get_json()
    assert "hostname" in data
    assert "cwd" in data
    assert "env" in data

# ------------------------
# Teste da função Monte Carlo diretamente
# ------------------------
def test_monte_carlo_pi():
    # Número pequeno para teste rápido
    pi_est = monte_carlo_pi(1000)
    assert 3.0 < pi_est < 3.5  # Valor esperado aproximado de pi

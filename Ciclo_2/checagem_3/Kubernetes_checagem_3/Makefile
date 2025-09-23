# ------------------------
# Makefile para Flask Monte Carlo
# ------------------------

# Variáveis
IMAGE_NAME = flask-montecarlo
DOCKER_PORT = 8080
KUBE_MANIFEST = kube-flask-montecarlo.yaml

# ------------------------
# Instalação de dependências Python
# ------------------------
install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

# ------------------------
# Linter / Verificação de estilo
# ------------------------
lint:
	# Lint Dockerfile
	docker run --rm -i hadolint/hadolint < Dockerfile
	# Lint código Python
	pylint --disable=R,C,W1203,W0702 app.py

# ------------------------
# Testes
# ------------------------
test:
	python -m pytest -vv --cov=app test_app.py

# ------------------------
# Build Docker
# ------------------------
build:
	docker build -t $(IMAGE_NAME):latest .

# ------------------------
# Rodar container Docker local
# ------------------------
run:
	docker run -p $(DOCKER_PORT):8080 $(IMAGE_NAME)

# ------------------------
# Teste endpoint local
# ------------------------
invoke:
	curl http://127.0.0.1:$(DOCKER_PORT)/montecarlo/1000000

docker-info:
	curl http://127.0.0.1:$(DOCKER_PORT)/docker-info

# ------------------------
# Kubernetes
# ------------------------
run-kube:
	kubectl apply -f $(KUBE_MANIFEST)

# ------------------------
# Alvo padrão: instala, linta e testa
# ------------------------
all: install lint test


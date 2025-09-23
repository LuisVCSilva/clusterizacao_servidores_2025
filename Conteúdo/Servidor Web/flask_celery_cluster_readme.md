# Flask + Celery - App para Aula de Clusterização

Este repositório contém um exemplo simples de aplicação web usando Flask e Celery, ideal para aulas sobre clusterização de servidores e processamento assíncrono distribuído.

---

## Descrição

A aplicação Flask funciona como uma API que recebe requisições para executar tarefas demoradas de forma assíncrona. Essas tarefas são enviadas para uma fila gerenciada pelo Celery, que usa o Redis como broker e backend de resultados.

O Celery executa as tarefas em workers separados, que podem rodar em máquinas diferentes, simulando um cluster de processamento distribuído.

---

## Tecnologias utilizadas

- **Python 3**
- **Flask**: microframework web para criação da API
- **Celery**: biblioteca para processamento assíncrono e distribuído de tarefas
- **Redis**: broker e backend para filas e armazenamento de resultados

---

## Estrutura do projeto

```
flask-celery-cluster/
├── app.py         # Configuração do Flask e Celery, endpoints da API
├── tasks.py       # Tarefas assíncronas definidas para execução
├── requirements.txt  # Dependências do projeto
└── README.md      # Documentação (este arquivo)
```

---

## Como executar

1. Instale o Redis e o inicie:

```bash
sudo apt install redis-server -y
sudo systemctl start redis
```

2. Instale as dependências Python:

```bash
pip install -r requirements.txt
```

3. Inicie o worker Celery:

```bash
celery -A app.celery worker --loglevel=info
```

4. Rode o servidor Flask:

```bash
python app.py
```

---

## Testando a aplicação

- Para iniciar uma tarefa assíncrona, envie uma requisição POST para `/longtask` com JSON:

```json
{"x": 10}
```

- Para consultar o status e resultado, faça GET para `/status/<task_id>`

---

## Conceitos abordados

- Arquitetura de processamento distribuído via filas de mensagens
- Desacoplamento do processamento pesado do servidor web
- Escalabilidade horizontal com múltiplos workers
- Uso de broker (Redis) para gerenciar filas de tarefas
- Monitoramento e consulta de tarefas assíncronas

---

## Atividade para a turma

- Modificar a aplicação para implementar uma tarefa que calcule o fatorial de um número de forma assíncrona.
- Criar endpoints para iniciar a tarefa e consultar o resultado.
- Rodar múltiplos workers para observar a escalabilidade do sistema.

---

Este projeto é uma base prática para entender clusterização e processamento distribuído em sistemas modernos.

---

**Boa aula!**

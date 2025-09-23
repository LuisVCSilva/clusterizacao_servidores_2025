from flask import Flask, jsonify, request, render_template_string
from celery import Celery
import time

app = Flask(__name__)

# Config Celery
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = Celery(
    app.import_name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)
celery.conf.update(app.config)


@celery.task(bind=True)
def factorial(self, n):
    time.sleep(1)  # Simula uma demora para ver efeito assíncrono
    if n < 0:
        raise ValueError("Número deve ser não-negativo")
    result = 1
    for i in range(2, n + 1):
        result *= i
        time.sleep(0.1)  # Simula trabalho pesado
    return result


@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
  <title>Flask + Celery Factorial Demo</title>
</head>
<body>
  <h1>Calcular Fatorial (Assíncrono)</h1>
  <input type="number" id="number" value="5" min="0" />
  <button onclick="startTask()">Calcular Fatorial</button>
  <p id="status">Insira um número e clique no botão.</p>
  <script>
    let taskId = null;

    function startTask() {
      const n = parseInt(document.getElementById('number').value);
      if (isNaN(n) || n < 0) {
        alert('Digite um número inteiro não-negativo');
        return;
      }
      document.getElementById('status').innerText = 'Iniciando cálculo...';
      fetch('/longtask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({number: n})
      })
      .then(response => response.json())
      .then(data => {
        taskId = data.task_id;
        document.getElementById('status').innerText = 'Tarefa iniciada. ID: ' + taskId;
        checkStatus();
      });
    }

    function checkStatus() {
      if (!taskId) return;
      fetch('/status/' + taskId)
        .then(response => response.json())
        .then(data => {
          if(data.state === 'PENDING') {
            document.getElementById('status').innerText = 'Status: Pendente...';
            setTimeout(checkStatus, 1000);
          } else if (data.state === 'SUCCESS') {
            document.getElementById('status').innerText = 'Resultado (Fatorial): ' + data.result;
          } else if (data.state === 'FAILURE') {
            document.getElementById('status').innerText = 'Falha: ' + data.status;
          } else {
            document.getElementById('status').innerText = 'Status: ' + data.state;
            setTimeout(checkStatus, 1000);
          }
        });
    }
  </script>
</body>
</html>
    """)


@app.route('/longtask', methods=['POST'])
def longtask():
    data = request.json or {}
    n = data.get('number', 5)
    task = factorial.delay(n)
    return jsonify({'task_id': task.id}), 202


@app.route('/status/<task_id>')
def task_status(task_id):
    task = factorial.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pendente...'}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    elif task.state == 'FAILURE':
        response = {'state': task.state, 'status': str(task.info)}
    else:
        response = {'state': task.state, 'status': 'Processando...'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

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

# Definição da tarefa
@celery.task(bind=True)
def add_together(self, x, y):
    time.sleep(5)  # simula tarefa longa
    return x + y


@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
  <title>Flask + Celery Demo</title>
</head>
<body>
  <h1>Flask + Celery Demo</h1>
  <button onclick="startTask()">Iniciar Tarefa</button>
  <p id="status">Clique no botão para iniciar a tarefa.</p>
  <script>
    let taskId = null;

    function startTask() {
      document.getElementById('status').innerText = 'Iniciando tarefa...';
      fetch('/longtask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x: 10})
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
            document.getElementById('status').innerText = 'Resultado: ' + data.result;
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
    x = data.get('x', 10)
    task = add_together.delay(x, x)
    return jsonify({'task_id': task.id}), 202


@app.route('/status/<task_id>')
def task_status(task_id):
    task = add_together.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    elif task.state == 'FAILURE':
        response = {'state': task.state, 'status': str(task.info)}
    else:
        response = {'state': task.state, 'status': 'Processando...'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, jsonify, request
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',           # Broker (exemplo: redis local)
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'        # Backend de resultado (redis local)
)

celery = make_celery(app)

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
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

from tasks import add_together

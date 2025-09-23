from app import celery
import time

@celery.task(bind=True)
def add_together(self, x, y):
    # Simula uma tarefa demorada (exemplo de clusterização)
    time.sleep(5)
    return x + y

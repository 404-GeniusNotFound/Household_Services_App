from celery_app import celery

result = celery.send_task('tasks.add', args=[4, 5])
print(result.get(timeout=10))

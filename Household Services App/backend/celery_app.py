# celery_app.py

from celery import Celery
from celery.schedules import crontab
from config_app import Config
from extensions import mail
from app import create_app

def make_celery():
    app = create_app()

    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        include=[
            'tasks.reminders',
            'tasks.reports',
            'tasks.exports',
        ]
    )

    celery.conf.update({
        'broker_connection_retry_on_startup': True,
        'worker_pool': 'solo',
    })

    celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'tasks.reminders.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),
    },
    'send-monthly-reports': {
        'task': 'tasks.reports.send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
    'export-closed-requests-daily': {
        'task': 'tasks.exports.export_closed_service_requests',
        'schedule': crontab(hour=0, minute=0),
        'args': ['admin@example.com'],
    },
}

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery()

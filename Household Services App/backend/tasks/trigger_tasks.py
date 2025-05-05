# tasks/trigger_tasks.py

from celery_app import celery
from tasks.exports import export_closed_service_requests
from tasks.reminders import send_daily_reminders
from tasks.reports import send_monthly_reports

if __name__ == "__main__":
    # Trigger export_closed_service_requests
    export_closed_service_requests.delay('admin@services.com')
    print("Triggered export_closed_service_requests")

    # Trigger send_daily_reminders
    send_daily_reminders.delay()
    print("Triggered send_daily_reminders")

    # Trigger send_monthly_reports
    send_monthly_reports.delay()
    print("Triggered send_monthly_reports")

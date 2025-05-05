# tasks/exports.py

import logging
from celery_app import celery
from flask_mail import Message
from models import ServiceRequest
from extensions import mail
import csv
from io import StringIO

logger = logging.getLogger(__name__)

@celery.task
def export_closed_service_requests(admin_email):
    try:
        print("Task export_closed_service_requests started")
        logger.info("Starting export_closed_service_requests task")

        closed_requests = ServiceRequest.query.filter(
            ServiceRequest.status.in_(['completed', 'rated'])
        ).all()
        print(f"Retrieved {len(closed_requests)} closed/rated service requests")
        logger.info(f"Retrieved {len(closed_requests)} closed/rated service requests")

        if not closed_requests:
            print("No closed or rated service requests found. Sending empty CSV.")
            logger.warning("No closed or rated service requests found. Sending empty CSV.")

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Remarks'])

        for req in closed_requests:
            writer.writerow([
                req.id,
                req.customer_id,
                req.professional_id,
                req.request_date.strftime('%Y-%m-%d %H:%M:%S') if req.request_date else '',
                req.remarks or ''
            ])
            print(f"Wrote ServiceRequest ID: {req.id}")

        csv_content = output.getvalue()
        print(f"CSV Content Length: {len(csv_content)} characters")
        logger.info(f"CSV Content Length: {len(csv_content)} characters")

        msg = Message(
            subject='Export of Closed/Rated Service Requests',
            recipients=[admin_email],
            body='Please find attached the CSV export of closed and rated service requests.'
        )
        msg.attach('closed_service_requests.csv', 'text/csv', csv_content)
        print("Email composed with CSV attachment") 

        mail.send(msg)
        print(f"Export email sent to {admin_email}")
        logger.info(f"Export email sent to {admin_email}")
    except Exception as e:
        print(f"Error in export_closed_service_requests task: {e}")
        logger.error(f"Error in export_closed_service_requests task: {e}")
        raise

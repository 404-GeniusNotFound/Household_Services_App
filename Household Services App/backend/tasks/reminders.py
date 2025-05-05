# tasks/reminders.py

import logging
from celery_app import celery
from flask_mail import Message
from models import Professional, ServiceRequest
from extensions import mail

logger = logging.getLogger(__name__)

@celery.task
def send_daily_reminders():
    try:
        logger.info("Starting send_daily_reminders task")
        
        pending_requests = (
            Professional.query.join(ServiceRequest, ServiceRequest.professional_id == Professional.id)
            .filter(ServiceRequest.status == 'assigned')
            .all()
        )

        logger.info(f"Found {len(pending_requests)} professionals with pending requests")

        for professional in pending_requests:
            msg = Message(
                subject='Pending Service Requests Reminder',
                recipients=[professional.email],
                body=(
                    f'Dear {professional.full_name},\n\n'
                    'You have pending service requests awaiting your action. '
                    'Please log in to your account to accept or reject them.\n\n'
                    'Best regards,\n'
                    'Service App Team'
                )
            )
            mail.send(msg)
            logger.info(f"Reminder email sent to {professional.email}")
    except Exception as e:
        logger.error(f"Error in send_daily_reminders task: {e}")
        raise

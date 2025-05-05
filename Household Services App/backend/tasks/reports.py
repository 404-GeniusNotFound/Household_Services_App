# tasks/reports.py

import logging
from celery_app import celery
from flask_mail import Message
from models import Customer, ServiceRequest
from datetime import datetime, timedelta
from flask import render_template
from extensions import mail

logger = logging.getLogger(__name__)

@celery.task
def send_monthly_reports():
    try:
        logger.info("Starting send_monthly_reports task")
        
        today = datetime.today()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        customers = Customer.query.all()
        logger.info(f"Found {len(customers)} customers")

        for customer in customers:
            service_requests = ServiceRequest.query.filter(
                ServiceRequest.customer_id == customer.id,
                ServiceRequest.request_date >= first_day_last_month,
                ServiceRequest.request_date <= last_day_last_month
            ).all()

            if service_requests:
                logger.info(f"Preparing report for {customer.email}")
                
                report_html = render_template(
                    'monthly_report.html',
                    customer=customer,
                    service_requests=service_requests,
                    first_day=first_day_last_month.strftime('%Y-%m-%d'),
                    last_day=last_day_last_month.strftime('%Y-%m-%d')
                )

                msg = Message(
                    subject='Your Monthly Activity Report',
                    recipients=[customer.email],
                    html=report_html
                )

                mail.send(msg)
                logger.info(f"Monthly report sent to {customer.email}")
    except Exception as e:
        logger.error(f"Error in send_monthly_reports task: {e}")
        raise

import logging
from app.models.email import Email
from app.database import db
from datetime import datetime
import pytz
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_scheduled_emails(self):
    """Task to queue individual email sending tasks for scheduled emails."""
    logger.info("Checking for scheduled emails to send.")

    singapore_tz = pytz.timezone('Asia/Singapore')
    current_time = datetime.now(singapore_tz)

    try:
        emails_to_send = Email.query.filter(
            Email.scheduled_at <= current_time,
            Email.status.in_(['scheduled', 'failed'])
        ).all()

        if not emails_to_send:
            logger.info("No emails found to send.")
            return

        logger.info(f"Found {len(emails_to_send)} emails to process.")

        for email in emails_to_send:
            send_single_email_task.delay(email.id)
            logger.info(f"Queued email (ID: {email.id}) to be sent.")

    except Exception as e:
        logger.error(f"Unexpected error while queuing emails: {e}")
        db.session.rollback()

    finally:
        logger.info("Finished queuing scheduled emails for sending.")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_single_email_task(self, email_id):
    """Task to send an individual email asynchronously."""
    email = Email.query.get(email_id)

    if not email:
        logger.error(f"Email with ID {email_id} not found.")
        return

    try:
        send_email(email.email_subject, email.email_content, "test@email.com")

        email.status = 'sent'
        db.session.commit()
        logger.info(f"Email (ID: {email.id}) sent successfully.")

    except Exception as e:
        email.status = 'failed'
        db.session.commit()
        logger.error(f"Failed to send email (ID: {email.id}): {e}")
        raise self.retry(exc=e)


def send_email(subject, content, recipients):
    """Function to simulate sending an email."""
    logger.info(f"Sending email to {recipients} with subject: {subject}")

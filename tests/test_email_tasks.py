import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.database import db
from app.models import Email
from app.tasks import send_scheduled_emails, send_single_email_task

class TestEmailTasks(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.db = SQLAlchemy(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()


    def tearDown(self):
        self.app_context.pop()

    @patch('app.tasks.Email.query')
    @patch('app.tasks.send_single_email_task.delay')
    @patch('app.tasks.db.session.commit')
    def test_send_scheduled_emails(self, mock_commit, mock_delay, mock_query):
        """Test that send_scheduled_emails queues emails properly."""
        email = MagicMock()
        email.id = 1
        email.email_subject = "Test Subject"
        email.email_content = "Test Content"
        email.status = "scheduled"
        email.scheduled_at = datetime.now(pytz.timezone('Asia/Singapore'))

        mock_query.filter.return_value.all.return_value = [email]

        send_scheduled_emails()

        mock_delay.assert_called_once_with(email.id)

    @patch('app.tasks.Email.query')
    @patch('app.tasks.db.session.commit')
    def test_send_scheduled_emails_no_emails(self, mock_commit, mock_query):
        """Test send_scheduled_emails with no emails to send."""
        mock_query.filter.return_value.all.return_value = []

        send_scheduled_emails()

        mock_commit.assert_not_called()
        mock_query.filter.return_value.all.assert_called_once()

if __name__ == '__main__':
    unittest.main()